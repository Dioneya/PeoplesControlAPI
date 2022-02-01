from plistlib import InvalidFileException
from flask import jsonify, request,url_for
from flask_jwt_extended import get_jwt_identity,jwt_required
from geopy.distance import geodesic as GD
from . import routes
from models import ApplicationCategories, ProblemCategories, RequestsModel, Users, ContractorsProblems
from api import db,app
from datetime import datetime
from page_manager import PagesManager
import errors_response
import tools
import json
from routes.servises_api import get_address
import os
from werkzeug.utils import secure_filename
from jsonschema import validate
from schemas import request_valide
from tg import bot
import hashlib

statuses = {
    "IN PROCESSING" : 1, 
    "IN CONSIDERATION" : 2, 
    "IN EXECUTION" : 3,
    "IN EXECUTION CHECK" : 4,
    "COMPLETED" : 5,
    "ARCHIVED" : 6
}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','mp4'}


@routes.route('/requests/<id>', methods=['GET'])
def get_request_by_id(id):
    """Получить зявку по ID"""

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id)

    res = db.session.query(RequestsModel).get(id)

    if res is None:
            return jsonify(errors_response.incorrect_id)
    
    return jsonify(res.json_view())


@routes.route('/requests', methods=['GET'])
def get_requests():
    """Получить список заявок"""

    res = db.session.query(RequestsModel).paginate(int(request.args.get('page',1)),int(request.args.get('size', 25)),error_out=False)
    return jsonify(PagesManager.generate_json_data(res,'requests')),200


@routes.route('/requests', methods=['POST'])
@jwt_required()
def create_requests():
    """Создать новую заявку"""

    try:
        json_data = json.loads(request.form['json_data'])
        validate(instance=json_data, schema=request_valide.scheme)
    except:
        return jsonify(errors_response.incorrect_data)

    user_id = get_jwt_identity()
    is_admin = tools.check_admin_mode(user_id)

    base_rating = json_data.get('base_rating', 0)
    request_consideration_at = json_data.get('request_consideration_at')
    begin_request_execution_at = json_data.get('begin_request_execution_at')
    complete_request_execution_at = json_data.get('complete_request_execution_at')
    request_status_checked_at = json_data.get('request_status_checked_at')
    status = statuses[json_data.get('status')] if json_data.get('status') is not None else 1
    is_moderated = json_data.get('is_moderated', False)
    moderator_id = json_data.get('moderator_id')

    #Проверка на попытку изменения полей, которые не должны быть доступны обычным пользователям
    if not is_admin and (json_data.get('base_rating') is not None or \
        request_consideration_at is not None or\
        begin_request_execution_at is not None or\
        complete_request_execution_at is not None or\
        request_status_checked_at is not None ) or\
        json_data.get('status') is not None or\
        json_data.get('is_moderated') is not None or\
        moderator_id  is not None:
            return jsonify(errors_response.low_accept_lvl),400

    if moderator_id is not None and db.session.query(Users).get(moderator_id) is None:
        return jsonify(errors_response.incorrect_data),400

    parent_id = json_data.get('parent_request_id')
    description = json_data.get('description')
    source = json_data.get('source')
    problem_categories = list(set(json_data.get('problem_categories',[])))
    latitude = json_data.get('latitude')
    longitude = json_data.get('longitude')

    #Заполнение базовой информации заявки
    elem = RequestsModel(
        user_id = user_id,
        address =  get_address(latitude,longitude),
        redirect_to_application_id  = parent_id,
        problem_desc = description,
        source = source,
        latitude = latitude,
        longitude = longitude,
        base_rate= base_rating,
        start_date = begin_request_execution_at\
                    if json_data.get("begin_request_execution_at") is None\
                    else datetime.strptime(begin_request_execution_at, "%Y-%m-%d %H:%M:%S"),
        review_date = request_consideration_at\
                    if json_data.get("request_consideration_at") is None\
                    else datetime.strptime(request_consideration_at, "%Y-%m-%d %H:%M:%S"),
        complete_date = complete_request_execution_at\
                    if json_data.get("complete_request_execution_at") is None\
                    else datetime.strptime(complete_request_execution_at, "%Y-%m-%d %H:%M:%S"),
        final_date = request_status_checked_at\
                    if json_data.get("request_status_checked_at ") is None\
                    else datetime.strptime(request_status_checked_at , "%Y-%m-%d %H:%M:%S"),
        status_id = status,
        is_moderate = is_moderated,
        moderator_id = moderator_id
    )  

    #Загрузка прикреплённых файлов на сервер
    try:
        attach = _upload_files(request)
        elem.media_data = json.dumps(attach if attach is not None else []) 
    except InvalidFileException:
        return jsonify(errors_response.incorrect_data),400

    db.session.add(elem)
    db.session.merge(elem)
    db.session.commit()

    #Заносим в БД связи с категориями
    for i in problem_categories:
        if type(i) != int or db.session.query(ProblemCategories).get(i) is None: continue
        _ = ApplicationCategories(application_id=elem.id, category_id=i)
        db.session.add(_)
        db.session.merge(_)
        db.session.commit()

    json_view = elem.json_view()
    bot.notify_contractor_in_telegram(request_data=_get_json_with_contractors(json_view))

    return jsonify(json_view),200


def _upload_files(request):

    res = [] # результат attachments
    files = request.files.getlist('files')
    for file in files:

        if file and _allowed_file(file.filename):
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(hashlib.md5(file.read()).hexdigest()+'.'+file_ext)
            file.seek(0, os.SEEK_END)
            file_length = file.tell() / 1048576 # получить размер файла в мб

            #Ограничение в 20 МБ для видео и 5 МБ для фото
            if (file_ext == 'mp4' and file_length > 20 ) or (file_ext != 'mp4' and file_length > 5):
                raise InvalidFileException
            
            file.seek(0) #Сброс указателя на 0
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            res.append(
                {
                    'type':'VIDEO' if file_ext == 'mp4' else 'IMAGE',
                    'url':url_for('routes.get_media', name=filename)
                }
            )

    return res


def _get_json_with_contractors(json_data:dict) -> dict:

    def _get_dict_contracotrs(problem_id)->list:
        return [_.categories_contract.json_view() for _ in db.session.query(ContractorsProblems).filter(
                    ContractorsProblems.problem_id == problem_id
                ).all()]
    
    tmp = []
    for _ in json_data.get('problem_categories',[]):
        tmp.extend(_get_dict_contracotrs(_.get('id')))

    print(tmp)
    json_data["contractors"] = tmp
    return json_data


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@routes.route('/requests/<id>', methods=['DELETE'])
@jwt_required()
def delete_requests_by_id(id):
    """Удалить заявку по ID"""

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id),400

    res = db.session.query(RequestsModel).get(id)
    if res is None:
            return jsonify(errors_response.non_existent_record),400

    user_id  = get_jwt_identity()
    if not tools.check_admin_mode(user_id) and res.user_id!=user_id:
        return jsonify(errors_response.low_accept_lvl),400

    if res.delete_date is not None:
        
        return jsonify(errors_response.record_already_deleted),400

    res.update_date = datetime.utcnow()
    res.delete_date = datetime.utcnow()

    db.session.merge(res)
    db.session.commit()

    return jsonify(res.json_view()),200


@routes.route('/requests/<id>', methods=['PUT'])
@app.validate( 'request', 'requsets_edit' )
@jwt_required()
def update_requests_by_id(id):
    """Обновить заявку по ID"""

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id),400

    res = db.session.query(RequestsModel).get(int(id))
    if res is None:
        return jsonify(errors_response.non_existent_record),400

    user_id = get_jwt_identity()
    is_admin = tools.check_admin_mode(user_id)

    #Имеет ли доступ к изменению данной заявки пользователь?
    if not is_admin and res.user_id!=user_id:
        return jsonify(errors_response.low_accept_lvl),400

    #Проверка на попытку изменения полей, которые не должны быть доступны обычным пользователям
    if not is_admin and (request.json.get('base_rating') is not None or \
        request.json.get('request_consideration_at') is not None or\
        request.json.get('begin_request_execution_at') is not None or\
        request.json.get('complete_request_execution_at') is not None or\
        request.json.get('request_status_checked_at') is not None ) or\
        request.json.get('status') is not None or\
        request.json.get('is_moderated') is not None or\
        request.json.get('moderator_id') is not None:
            return jsonify(errors_response.low_accept_lvl),400

   

    #Параметры заявки
    base_rating = request.json.get('base_rating', res.base_rate)
    request_consideration_at = request.json.get('request_consideration_at', res.review_date)
    begin_request_execution_at = request.json.get('begin_request_execution_at', res.start_date)
    complete_request_execution_at = request.json.get('complete_request_execution_at', res.complete_date)
    request_status_checked_at = request.json.get('request_status_checked_at', res.final_date)
    status = statuses[request.json.get('status')] if request.json.get('status') is not None else res.status_id
    is_moderated = request.json.get('is_moderated',res.is_moderate)
    moderator_id = request.json.get('moderator_id',res.moderator_id)
    source = request.json.get('source', res.source)
    parent_id = request.json.get('parent_request_id',res.redirect_to_application_id)
    description = request.json.get('description', res.problem_desc)
    problem_categories = list(set(request.json.get('problem_categories',[])))
    latitude = request.json.get('latitude', res.latitude)
    longitude = request.json.get('longitude', res.longitude)
    attachments = request.json.get('attachments',res.media_data)

    if moderator_id is not None and db.session.query(Users).get(moderator_id) is None:
        return jsonify(errors_response.incorrect_data),400

    #Проверка на существующие проблемные категории
    for i in problem_categories:
        if db.session.query(ProblemCategories).get(i) is None:
            return errors_response.incorrect_data

    #Перезаписывание параметров 
    res.redirect_to_application_id = parent_id
    res.problem_desc = description
    res.source = source
    res.latitude = latitude
    res.longitude = longitude
    res.media_data = attachments
    res.base_rate = base_rating
    res.moderator_id = moderator_id
    res.is_moderate = is_moderated
    res.start_date = begin_request_execution_at\
                        if request.json.get("begin_request_execution_at") is None\
                        else datetime.strptime(begin_request_execution_at, "%Y-%m-%d %H:%M:%S")
    res.review_date = request_consideration_at\
                        if request.json.get("request_consideration_at") is None\
                        else datetime.strptime(request_consideration_at, "%Y-%m-%d %H:%M:%S")
    res.complete_date = complete_request_execution_at\
                        if request.json.get("complete_request_execution_at") is None\
                        else datetime.strptime(complete_request_execution_at, "%Y-%m-%d %H:%M:%S")
    res.final_date = request_status_checked_at\
                        if request.json.get("request_status_checked_at ") is None\
                        else datetime.strptime(request_status_checked_at , "%Y-%m-%d %H:%M:%S")
    res.status_id = status
    res.update_date = datetime.utcnow()
    db.session.add(res)
    db.session.merge(res)
    db.session.commit()

    if problem_categories != []:

        for elem in res.categories:
            db.session.query(ApplicationCategories).filter(ApplicationCategories.id == elem.id).delete()
            db.session.commit()    

        for elem in problem_categories:
            element = ApplicationCategories(application_id = id, category_id = elem)
            db.session.add(element)
            db.session.merge(element)
            db.session.commit()
    
    

    return jsonify(res.json_view()),200
    

@routes.route('/requests/in-range', methods=['POST'])
def get_in_range():
    """Получить заявки по радиусу"""

    distance = request.json.get('distance')
    longitude = request.json.get('longitude')
    latitude = request.json.get('latitude') 

    if type(distance) != int and type(distance)!=float:
        return errors_response.incorrect_data

    person_point = (latitude,longitude)
    res = db.session.query(RequestsModel).all()
    return jsonify([ _.json_view() for _ in res if GD(person_point,(_.latitude,_.longitude)).m<=distance ]),200


@routes.route('/requests/<id>/watch', methods=['POST'])
@jwt_required()
def add_watch(id):
    """Добавить просмотр заявке"""
    
    user_id = get_jwt_identity()
    if type(user_id) is not int or db.session.query(Users).get(user_id) is None or not id.isdigit():
        return errors_response.incorrect_data

    res = db.session.query(RequestsModel).get(int(id))
    if res is None:
        return errors_response.non_existent_record
    
    if res.user_id == user_id:
        return jsonify(),200

    res.views_count+=1
    db.session.add(res)
    db.session.merge(res)
    db.session.commit()
    return jsonify('OK'),200
