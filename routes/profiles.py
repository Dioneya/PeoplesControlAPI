from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity,jwt_required
from . import routes
from models import Users, UsersProfiles
from api import db,app
from datetime import datetime
from page_manager import PagesManager
import errors_response
import tools


@routes.route('/profiles', methods=['GET'])
@jwt_required()
def get_profiles():
    
    if not tools.check_admin_mode(get_jwt_identity()):
        return jsonify(errors_response.low_accept_lvl)

    res = db.session.query(UsersProfiles).paginate(int(request.args.get('page',1)),int(request.args.get('size', 25)),error_out=False)
    return jsonify(PagesManager.generate_json_data(res,'profiles')),200


@routes.route('/profiles/<id>', methods=['GET'])
@jwt_required()
def get_profile_by_id(id):

    user_id = get_jwt_identity()
    
    if type(user_id) is not int or not id.isdigit():
        return errors_response.incorrect_data

    res = db.session.query(UsersProfiles).get(id)
    if res is None:
        return errors_response.non_existent_record
    
    if not tools.check_admin_mode(user_id) or res.user_id != user_id :
        return jsonify(errors_response.low_accept_lvl)

    return jsonify(res.json_view()),200


@routes.route('/profile', methods=['GET'])
@jwt_required()
def get_profile_user():

    user_id = get_jwt_identity()

    if type(user_id) is not int:
        return errors_response.incorrect_data

    res = db.session.query(UsersProfiles).filter(UsersProfiles.user_id == user_id).first()
    if res is None:
        return errors_response.non_existent_record
    
    return jsonify(res.json_view()), 200


@routes.route('/profiles/<id>', methods=['PUT'])
@app.validate( 'profile', 'profile_edit' )
@jwt_required()
def update_profile(id):

    user_id = get_jwt_identity()
    
    if type(user_id) is not int or not id.isdigit():
        return errors_response.incorrect_data

    res = db.session.query(UsersProfiles).get(id)
    if res is None:
        return errors_response.non_existent_record
    
    is_admin = tools.check_admin_mode(user_id)
    if not is_admin and res.user_id != user_id :
        return jsonify(errors_response.low_accept_lvl)
    
    res.name = request.json.get('full_name', res.name)
    res.location = request.json.get('location', res.location)
    res.phone_number = request.json.get('phone',res.phone_number)
    res.email = request.json.get('email',res.email)
    res.is_email_alert = request.json.get('is_notification_email', res.is_email_alert)
    res.is_sms_alert = request.json.get('is_notification_sms', res.is_sms_alert)
    res.is_anonym = request.json.get('is_anonymous_request', res.is_anonym)
    res.update_date = datetime.utcnow()

    if is_admin:
        user_id = request.json.get('user_id',res.user_id)
        if type(user_id) != int or db.session.query(Users).get(user_id) is None:
            return errors_response.incorrect_data
        res.user_id = user_id

    db.session.add(res)
    db.session.merge(res)
    db.session.commit()

    return jsonify(res.json_view()), 200


@routes.route('/profiles/<id>', methods=['DELETE'])
@jwt_required()
def delete_profile(id):

    if not id.isdigit():
        return jsonify(errors_response.incorrect_id),400

    res = db.session.query(UsersProfiles).get(id)
    if res is None:
        return errors_response.non_existent_record

    user_id = get_jwt_identity()
    is_admin = tools.check_admin_mode(user_id)
    
    if not is_admin and res.user_id != user_id :
        return jsonify(errors_response.low_accept_lvl)

    if res.delete_date is not None:
        return jsonify(errors_response.record_already_deleted),400

    res.update_date = datetime.utcnow()
    res.delete_date = datetime.utcnow()

    db.session.merge(res)
    db.session.commit()

    return jsonify(res.json_view()),200


