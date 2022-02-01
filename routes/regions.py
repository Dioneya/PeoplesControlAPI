from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity,jwt_required
from . import routes
import tools
from models import Region
from api import db
from datetime import datetime
import errors_response
from page_manager import PagesManager

   
@routes.route('/regions', methods=['GET'])
def getRegions():

    res = db.session.query(Region).paginate(int(request.args.get('page',1)),int(request.args.get('size', 25)),error_out=False)
    return jsonify(PagesManager.generate_json_data(res,'regions')),200


@routes.route('/regions/<id>', methods=['GET'])
@jwt_required()
def getRegionsById(id):

    res = db.session.query(Region).get(id)

    try:
        return jsonify({
            "id": res.id,
            "title": res.title,
            "positions": res.position,
            "is_active": res.is_available,
            "deleted_at": str(res.delete_date),
            "created_at": str(res.create_date),
            "updated_at": str(res.update_date)
        }),200

    except:
        return jsonify(errors_response.empty_id),400


@routes.route('/regions/<id>', methods=['PUT'])
@jwt_required()
def updateRegionsById(id):

    try:
        if not tools.check_admin_mode(get_jwt_identity()):
            return jsonify(errors_response.low_accept_lvl)
        res = db.session.query(Region).get(id)
        if res is None:
            return jsonify(errors_response.non_existent_record),400

        res.id = request.json.get('id',res.id)
        res.title =  request.json.get('title',res.title)
        res.position = request.json.get('positions', res.position)
        res.is_available = request.json.get('is_active',res.is_available)
        res.update_date = datetime.utcnow()

        db.session.merge(res)
        db.session.commit()

        return jsonify(res.json_view()),200
        
    except:
        return jsonify(errors_response.empty_id),400


@routes.route('/regions/<id>', methods=['DELETE'])
@jwt_required()
def delete_region(id):

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id),400

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl)

    res = db.session.query(Region).get(id)
    if res is None:
        
            return jsonify(errors_response.non_existent_record),400

    if res.delete_date is not None:
        
        return jsonify(errors_response.record_already_deleted),400

    res.delete_date = datetime.utcnow()

    db.session.merge(res)
    db.session.commit()

    return jsonify(res.json_view()),200


@routes.route('/regions', methods=['POST'])
@jwt_required()
def create_new_region():

    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl)

    _title = request.json.get('title')
    _positions = request.json.get('positions')
    _is_active = request.json.get('is_active')
    if type(_is_active) != bool or type(_positions) != int or type(_title)!=str or not _title.isalpha():
        return jsonify(errors_response.incorrect_data),400

    elem = Region(
        title = _title,
        position = _positions,
        is_available = _is_active,
        create_date = datetime.utcnow(),
        update_date = datetime.utcnow(),
        delete_date = None
    )

    db.session.add(elem)
    db.session.merge(elem)
    db.session.commit()

    return jsonify(elem.json_view()),200
