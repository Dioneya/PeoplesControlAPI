from models import Users
from api import db

def check_admin_mode(id):

    user = db.session.query(Users).get(id)
    return user is not None and user.role_id == 1


def check_for_empty(value,tmp_value):
    
    return tmp_value if value is None else value