from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity,jwt_required, get_jwt
from . import routes
from datetime import datetime,timezone
import api
from models import Users, UsersProfiles
import errors_response

@routes.route('/auth/login', methods=['POST'])
def login():
    """Авторизация пользователя в системе"""

    try:
        login = request.json.get('username')
        password = request.json.get('password')

        res = api.db.session.query(Users).filter(Users.login == login, Users.password == password).first()

        if res is None:
            return jsonify({
                "title": "Ошибка входа",
                "message": "Неверный логин или пароль",
                "code": 400
            }),400

        access_token = create_access_token(identity=res.id, fresh=True)
        refresh_token = create_refresh_token(identity=res.id)
        
        return jsonify({
                "accessToken": access_token,
                "refreshToken" : refresh_token,
                "typeToken" : "Bearer"
            }),200
    except:
        return jsonify(errors_response.unexpected_error),400


@routes.route("/auth/logout", methods=["POST"])
@jwt_required()
def modify_token():
    """Выход из системы"""

    try:
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        api.db.session.add(api.TokenBlocklist(jti=jti, created_at=now))
        api.db.session.commit()
        return jsonify(msg="JWT revoked")
    except:
        return jsonify(errors_response.unexpected_error),400


@routes.route("/auth/refreshtoken", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """Обновление тоукена доступа"""

    try:
        id = get_jwt_identity()
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        api.db.session.add(api.TokenBlocklist(jti=jti, created_at=now))
        api.db.session.commit()

        access_token = create_access_token(identity=id, fresh=True)
        new_refresh_token = create_refresh_token(identity=id)

        return jsonify({
                    "accessToken": access_token,
                    "refreshToken" : new_refresh_token,
                    "typeToken" : "Bearer"
                }),200
    except:
        return jsonify(errors_response.unexpected_error)
   

@routes.route("/auth/signup", methods=["POST"])
@api.app.validate( 'users', 'register' )
def signup():
    """Регистрация нового пользователя"""

    try:
        name = request.json['name']
        username = request.json['username']
        password = request.json['password']

        if api.db.session.query(Users).filter(Users.login == username).first() is not None:
            return errors_response.registration_error

        user = Users(login = username, password = password, role_id=2)
        api.db.session.add(user)
        api.db.session.merge(user)

        user_profile = UsersProfiles(user_id = user.id, name = name)
        api.db.session.add(user_profile)

        
        api.db.session.merge(user_profile)
        api.db.session.commit()
    
    except:
        return jsonify(errors_response.unexpected_error)

    return jsonify({"message": "OK"})




