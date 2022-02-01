from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity,jwt_required
from . import routes
from models import Roles
from api import db, app
from datetime import datetime
from page_manager import PagesManager
import errors_response
import tools


@routes.route('/roles', methods=['GET'])
@jwt_required()
def get_roles():
    """Получить список ролей пользователей"""

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl)
        
    res = db.session.query(Roles).paginate(int(request.args.get('page',1)),int(request.args.get('size', 25)),error_out=False)
    return jsonify(PagesManager.generate_json_data(res,'roles')),200


@routes.route('/roles/<id>', methods=['GET'])
@jwt_required()
def get_role_by_id(id):
    """Получить роль пользователя по ID"""

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl)

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id)

    try:
        res = db.session.query(Roles).get(id)

        if res is None:
            return jsonify(errors_response.incorrect_id)
    
        return jsonify(res.json_view()),200

    except:
        return jsonify(errors_response.empty_id),400


@routes.route('/roles', methods=['POST'])
@app.validate('roles','roles')
@jwt_required()
def create_new_role():
    """Создать новую роль"""

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl),400

    elem = Roles(
        title = request.json['title'],
        mnemomic_name = request.json['slug'],
        create_date = datetime.utcnow(),
        update_date = datetime.utcnow(),
        delete_date = None
    )

    db.session.add(elem)
    db.session.merge(elem)
    db.session.commit()

    return jsonify(elem.json_view()),200


@routes.route('/roles/<id>', methods=['DELETE'])
@jwt_required()
def delete_role_by_id(id):
    """Удалить роль по ID"""

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl),400

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id),400

    res = db.session.query(Roles).get(id)
    if res is None:
            return jsonify(errors_response.non_existent_record),400

    if res.delete_date is not None:
        
        return jsonify(errors_response.record_already_deleted),400

    res.update_date = datetime.utcnow()
    res.delete_date = datetime.utcnow()

    db.session.merge(res)
    db.session.commit()

    return jsonify(res.json_view()),200


@routes.route('/roles/<id>', methods=['PUT'])
@app.validate('roles','role_update')
@jwt_required()
def update_role_by_id(id):
    """Обновить роль по ID"""

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl),400

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id),400

    res = db.session.query(Roles).get(id)
    if res is None:
            return jsonify(errors_response.non_existent_record),400

    res.title = request.json.get('title', res.title)
    res.mnemomic_name = request.json.get('slug', res.mnemomic_name)
    res.update_date = datetime.utcnow()

    db.session.merge(res)
    db.session.commit()

    return jsonify(res.json_view()), 200

