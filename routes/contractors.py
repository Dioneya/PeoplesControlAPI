from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity,jwt_required
import sqlalchemy
from . import routes
from models import Contractors, ContractorsProblems, ProblemCategories
from api import db,app
from datetime import datetime
from page_manager import PagesManager
import errors_response
import tools
import json

@routes.route('/contractors/<id>', methods=['GET'])
def get_contractor_by_id(id):
    """Находим исполнителя по ID"""

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id)

    try:
        res = db.session.query(Contractors).get(id)

        if res is None:
            return jsonify(errors_response.incorrect_id)
    
        return jsonify(res.json_view()),200

    except:
        return jsonify(errors_response.empty_id),400


@routes.route('/contractors/<id>', methods=['DELETE'])
@jwt_required()
def delete_contractor_by_id(id):
    """Удаление исполнителя по ID"""

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl),400

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id),400

    res = db.session.query(Contractors).get(id)
    if res is None:
            return jsonify(errors_response.non_existent_record),400

    if res.delete_date is not None:
        
        return jsonify(errors_response.record_already_deleted),400

    res.update_date = datetime.utcnow()
    res.delete_date = datetime.utcnow()

    db.session.merge(res)
    db.session.commit()

    return jsonify(res.json_view()),200


@routes.route('/contractors', methods = ['POST'])
@app.validate( 'contractors', 'contractor' )
@jwt_required()
def create_contractor():
    """Создаём профиль исполнительного органа"""

    try:
        if not tools.check_admin_mode(get_jwt_identity()):
            return jsonify(errors_response.low_accept_lvl),400

        elem = Contractors(
            title = request.json.get('title'),
            mnemomic_name = request.json.get('mnemonic_name'),
            description = request.json.get('description'),
            responsible_person = request.json.get('responsible_person'),
            image = request.json.get('image'),
            hash_tag = request.json.get('hash_tag'),
            contact_phone = request.json.get('contact_phone'),
            contact_email = request.json.get('contact_email'),
            contact_email_administration = request.json.get('pre_controller_email'),
            tg_id = request.json.get('telegram_chat_id'),
            web_site_link = request.json.get('public_website'),
            additional_information = request.json.get('more_info'),
            type = request.json.get('type'),
            work_schedule = json.dumps(request.json.get('schedule',[])),
            is_email_alert = request.json.get('need_inform_by_email',False),
            is_sms_alert = request.json.get('need_inform_by_sms', False),
            is_generate_daily_report = request.json.get('generate_daily_report', False),
            is_visible = request.json.get('is_active', False)
        )

        db.session.add(elem)
        db.session.merge(elem)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError:
        return jsonify(errors_response.dublicate_error),400


    #Заносим в БД связи с категориями
    for i in request.json.get('problem_categories',[]):
        
        if type(i) != int or db.session.query(ProblemCategories).get(i) is None: continue
        _ = ContractorsProblems(contractor_id=elem.id, problem_id=i)
        db.session.add(_)
        db.session.merge(_)
        db.session.commit() 
         

    return jsonify(elem.json_view()), 200


@routes.route('/contractors', methods=['GET'])
def get_contractors():
    """Список профилей исполнительных органов"""

    res = db.session.query(Contractors).paginate(int(request.args.get('page',1)),int(request.args.get('size', 25)),error_out=False)
    return jsonify(PagesManager.generate_json_data(res,'roles')),200