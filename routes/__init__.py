import imp
from flask import Blueprint
from flask_jsonschema_validator import JSONSchemaValidator

routes = Blueprint('routes', __name__)

from .authorization import *
from .regions import *
from .roles import *
from .problem_categories import *
from .requests_api import *
from .profiles import *
from .servises_api import *
from .contractors import *