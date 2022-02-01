import json
from flask import Flask, jsonify, request, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_session import flask_scoped_session
from flask_jwt_extended import create_access_token, create_refresh_token,JWTManager,get_jwt_identity,jwt_required
from datetime import datetime
from flask_jsonschema_validator import JSONSchemaValidator
import jsonschema


UPLOAD_FOLDER = './images/requests'

DOMAIN_NAME = "http://164.92.215.12:8644"
IMAGE_FOLDER = './img'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/hackaton'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'gfj454jklgfdkltjlrd554ggg'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
JSONSchemaValidator( app = app, root = "schemas" )
engine_options = {
    "max_overflow": 30,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "pool_size": 30,
    'connect_args': { 'connect_timeout': 3700 }
}

jwt = JWTManager(app)
db = SQLAlchemy(app,engine_options=engine_options)
#run_with_ngrok(app)
from routes import *

app.register_blueprint(routes)


class TokenBlocklist(db.Model):

    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<regions {self.id}>"


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None 


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.errorhandler( jsonschema.ValidationError )
def onValidationError( e ):
  return jsonify(errors_response.incorrect_data),400

if __name__ == '__main__':
    app.run()