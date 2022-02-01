from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity,jwt_required
from . import routes
from models import ProblemCategories, ApplicationCategories, RequestsModel
from api import db
from datetime import datetime
from page_manager import PagesManager
import errors_response
import tools


@routes.route('/problem-categories/<id>', methods=['GET'])
def get_category_by_id(id):
    """Находим категорию проблем по ID"""

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id)

    try:
        res = db.session.query(ProblemCategories).get(id)
        if res is None:
            return jsonify(errors_response.incorrect_id)
    
        return jsonify(res.json_view()),200

    except:
        return jsonify(errors_response.empty_id),400


@routes.route('/problem-categories', methods=['GET'])
def get_categories():
    """Получить список категорий проблем"""

    try:
        res = db.session.query(ProblemCategories).paginate(int(request.args.get('page',1)),int(request.args.get('size', 25)),error_out=False)
        return jsonify(PagesManager.generate_json_data(res,'problem-categories')),200
    except:
        return jsonify(errors_response.unexpected_error)


@routes.route('/problem-categories/<id>', methods=['PUT'])
@jwt_required()
def update_category_by_id(id):
    """Обновляем категорию проблем по ID"""

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl),400

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id),400

    try:
        res = db.session.query(ProblemCategories).get(id)
        if res is None:
                return jsonify(errors_response.non_existent_record),400

        title = request.json.get('title', res.title)
        slug = request.json.get('mnemomic_name', res.mnemomic_name)
        hash_code = request.json.get('hash_code', res.hash_code)
        icon = request.json.get('icon', res.icon_file_path)
        is_active = request.json.get('is_active', res.is_active)
        is_visible = request.json.get('is_visible', res.is_visible)

        if title == res.title and slug == res.mnemomic_name and \
        hash_code == res.hash_code and res.icon_file_path == icon and \
        is_active == res.is_active and is_visible == res.is_visible:
            return jsonify(errors_response.incorrect_data)

        if not is_data_valide(title,slug,hash_code,icon,is_active,is_visible):
            return jsonify(errors_response.incorrect_data)

        res.title = title
        res.mnemomic_name = slug
        res.hash_code = hash_code
        res.icon_file_path = icon
        res.is_active = is_active
        res.is_visible = is_visible
        res.update_date = datetime.utcnow()

        db.session.merge(res)
        db.session.commit()

        return jsonify(res.json_view()), 200

    except:
        return jsonify(errors_response.unexpected_error)


@routes.route('/problem-categories', methods=['POST'])
@jwt_required()
def create_category():
    """Создание категории проблем"""

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl),400

    try:
        _title = request.json.get('title')
        _slug = request.json.get('mnemomic_name')
        _hash_code = request.json.get('hash_code')
        _icon = request.json.get('icon')
        _is_active = request.json.get('is_active', False)
        _is_visible = request.json.get('is_visible', False)

        if not is_data_valide(_title,_slug,_hash_code,_icon,_is_active,_is_visible):
            return jsonify(errors_response.incorrect_data)

        elem = ProblemCategories(
            title = _title,
            mnemomic_name = _slug,
            hash_code = _hash_code,
            icon_file_path = _icon,
            is_active = _is_active,
            is_visible = _is_visible,
            create_date = datetime.utcnow(),
            update_date = datetime.utcnow(),
            delete_date = None
        )

        db.session.add(elem)
        db.session.merge(elem)
        db.session.commit()

        return jsonify(elem.json_view()),200

    except:
        return jsonify(errors_response.unexpected_error),400


@routes.route('/problem-categories/<id>', methods=['DELETE'])
@jwt_required()
def delete_category_by_id(id):
    """Удалить категорию проблем оп ID"""

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl),400

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id),400

    res = db.session.query(ProblemCategories).get(id)
    if res is None:
            return jsonify(errors_response.non_existent_record),400

    if res.delete_date is not None:
        
        return jsonify(errors_response.record_already_deleted),400

    res.update_date = datetime.utcnow()
    res.delete_date = datetime.utcnow()

    db.session.merge(res)
    db.session.commit()

    return jsonify(res.json_view()),200


@routes.route('/problem-categories/<id>/active-requests', methods=['GET'])
def get_active_req_from_category(id):
    """Получить активные запросы по ID категории проблемы"""

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id)

    size = int(request.args.get('size', 25))
    page = int(request.args.get('page',1))

    res = db.session.query(ApplicationCategories).filter(
            ApplicationCategories.category_id==id,
            RequestsModel.status_id < 5,
            RequestsModel.status_id > 1 ).join(RequestsModel).paginate(page,size,error_out=False)
    
    json_data = PagesManager.generate_json_data(res,f'problem-categories/{id}/active-requests',is_generate_data=False)
    json_data['data'] = [_.categories_appl.json_view() for _ in res.items]
    return jsonify(json_data),200
    
    
@routes.route('/problem-categories/<id>/archive-requests', methods=['GET'])
def get_archive_req_from_category(id):
    """Получить архивные запросы по ID категории проблемы"""

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id)

    size = request.args.get('size', 25)
    page = request.args.get('page',1)

    res = db.session.query(ApplicationCategories).join(RequestsModel).filter(
            ApplicationCategories.category_id == id, 
            RequestsModel.status_id == 6).paginate(page,size,error_out=False)

    json_data = PagesManager.generate_json_data(res,f'problem-categories/{id}/archive-requests',is_generate_data=False)
    json_data['data'] = [_.categories_appl.json_view() for _ in res.items]

    return jsonify(json_data),200


@routes.route('/problem-categories/<id>/completed-requests', methods=['GET'])
def get_completed_requests_from_category(id):
    """Получить выполненные запросы по ID категории проблемы"""
    
    if not id.isdigit():
        return jsonify(errors_response.incorrect_id)

    size = request.args.get('size', 25)
    page = request.args.get('page',1)

    res = db.session.query(
        ApplicationCategories).join(RequestsModel).filter(
            ApplicationCategories.category_id == id, 
            RequestsModel.status_id == 5).paginate(page,size,error_out=False)

    json_data = PagesManager.generate_json_data(res,f'problem-categories/{id}/completed-requests',is_generate_data=False)
    json_data['data'] = [_.categories_appl.json_view() for _ in res.items]

    return jsonify(json_data),200
    
#ПЕРЕДЕЛАТЬ ПОД JSON Schema Validation!!!
def is_data_valide(title, slug, hash_code, icon, is_active, is_visible):
    """Валидация данных"""

    is_title_valide = type(title) == str
    is_hash_invalid = hash_code is not None and (type(hash_code != str) or hash_code[0]!='#')
    is_slug_valide = type(slug) == str
    is_icon_valide = icon is None or type(icon) == str 
    is_active_valide = type(is_active) == bool
    is_visible_valide =  type(is_visible) == bool

    return is_title_valide and not is_hash_invalid and \
           is_slug_valide and is_icon_valide and \
           is_active_valide and is_visible_valide
