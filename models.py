from flask_sqlalchemy import SQLAlchemy
from api import db
from datetime import datetime
import json

class Region(db.Model):

    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    is_available = db.Column(db.Boolean)
    position = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    delete_date = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f"<regions {self.id}>"

    
    def json_view(self):

        return {
            "id": self.id,
            "title": self.title,
            "positions": self.position,
            "is_active": self.is_available,
            "deleted_at": str(self.delete_date) if self.delete_date is not None else None,
            "created_at": str(self.create_date),
            "updated_at": str(self.update_date)
        }


class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    sms_code = db.Column(db.String(4))
    email_code = db.Column(db.String(255), unique = True)
    phone_confirm_date = db.Column(db.DateTime, default = None)
    email_confirm_date = db.Column(db.DateTime, default = None)
    ban_date = db.Column(db.DateTime, default = None)
    delete_date = db.Column(db.DateTime, default = None)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)

    tasks =  db.relationship('RequestsModel', backref='users_task',
                                lazy='dynamic',primaryjoin="Users.id == RequestsModel.user_id")
    moder_task = db.relationship('RequestsModel', backref='moder_task',
                                lazy='dynamic',primaryjoin="Users.id == RequestsModel.moderator_id")

    user_profile = db.relationship('UsersProfiles', backref='profile', uselist=False,primaryjoin="Users.id ==UsersProfiles.user_id")
    
    def __repr__(self):
        return f"<user {self.id}>"


class UsersProfiles(db.Model):

    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),default = None) 
    name = db.Column(db.String(255))
    phone_number = db.Column(db.String(20), default = None)
    email = db.Column(db.String(50),default = None)
    location = db.Column(db.String(255), default = None)
    is_email_alert = db.Column(db.Boolean, default = False)
    is_sms_alert  = db.Column(db.Boolean, default = False)
    is_anonym  = db.Column(db.Boolean, default = False)
    delete_date = db.Column(db.DateTime, default = None)
    update_date = db.Column(db.DateTime, default = datetime.utcnow)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    rate = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f"<user_profile {self.id}>"


    def json_view(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.name,
            "location": self.location,
            "phone": self.phone_number,
            "rating": self.rate,
            "email": self.email,
            "requests": [
                _.json_view() for _ in self.profile.tasks
            ],
            "stored_requests": [
                # {
                # "id": 1,
                # "user_id": 1,
                # "description": "Описание заявки",
                # "problem_categories": [
                #     {
                #     "id": 1,
                #     "title": "Яма на дороге",
                #     "mnemonic_name": "yama_na_doroge",
                #     "hash_tag": "#дорожное_движение",
                #     "icon": "https://test.com/123.jpg",
                #     "rating": 10,
                #     "is_active": true,
                #     "is_visible": true,
                #     "deleted_at": "2022-01-01 12:00:00",
                #     "created_at": "2022-01-01 12:00:00",
                #     "updated_at": "2022-01-01 12:00:00"
                #     }
                # ],
                # "latitude": 23.2334444,
                # "longitude": 45.7889111,
                # "attachments": [],
                # "deleted_at": "2022-01-01 12:00:00",
                # "created_at": "2022-01-01 12:00:00",
                # "updated_at": "2022-01-01 12:00:00"
                # }
            ],
            "is_notification_email": self.is_email_alert,
            "is_notification_sms": self.is_sms_alert,
            "is_anonymous_requests": self.is_anonym,
            "deleted_at": str(self.delete_date) if self.delete_date is not None else None,
            "created_at": str(self.create_date),
            "updated_at": str(self.update_date)
        }


class Roles(db.Model):

    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), unique = True)
    mnemomic_name = db.Column(db.String(50), default = None)
    delete_date = db.Column(db.DateTime, default = None)
    update_date = db.Column(db.DateTime, default = datetime.utcnow)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('Users', backref='roles',
                                lazy='dynamic',primaryjoin="Roles.id == Users.role_id")

    def __repr__(self):
        return f"<role {self.id}>"


    def json_view(self):

        return {
            "id": self.id,
            "title": self.title,
            "slug": self.mnemomic_name,
            "deleted_at": str(self.delete_date) if self.delete_date is not None else None,
            "created_at": str(self.create_date),
            "updated_at": str(self.update_date)
        }


class ProblemCategories(db.Model):

    __tablename__= 'problem_categories'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique = True)
    mnemonic_name = db.Column(db.String(100), default = None)
    hash_tag = db.Column(db.String(100), default = None)
    icon_file_path = db.Column(db.String(255),default = None)
    is_active = db.Column(db.Boolean, default = False)
    is_visible =  db.Column(db.Boolean, default = False)
    priority = db.Column(db.Integer, default = 0)
    delete_date = db.Column(db.DateTime, default = None)
    update_date = db.Column(db.DateTime, default = datetime.utcnow)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('ApplicationCategories', backref='categories_applic',
                                lazy='dynamic',primaryjoin="ProblemCategories.id == ApplicationCategories.category_id")
    contractors = db.relationship('ContractorsProblems', backref='categories_contracts', 
                                lazy='dynamic',primaryjoin="ProblemCategories.id == ContractorsProblems.problem_id")

    def __repr__(self):
        return f"<regions {self.id}>"


    def json_view(self):

        return {
            "id": self.id,
            "title": self.title,
            "mnemonic_name": self.mnemonic_name,
            "hash_tag": self.hash_tag,
            "icon": self.icon_file_path,
            "rating": self.priority,
            "is_active": self.is_active,
            "is_visible": self.is_visible,
            "deleted_at": str(self.delete_date) if self.delete_date is not None else None,
            "created_at": str(self.create_date),
            "updated_at": str(self.update_date)
        }


class ApplicationStatus(db.Model):

    __tablename__ = 'application_status'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), unique = True)

    tasks = db.relationship('RequestsModel', backref='application_status',
                                lazy='dynamic',primaryjoin="ApplicationStatus.id == RequestsModel.status_id")
    def __repr__(self):
        return f"<application_status {self.id}>"


class ApplicationCategories(db.Model):

    __tablename__ = 'applications_categories'

    id = db.Column(db.Integer, primary_key = True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('problem_categories.id'))

    
class RequestsModel(db.Model):

    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    redirect_to_application_id = db.Column(db.Integer, db.ForeignKey('applications.id')) 
    address = db.Column(db.String(255), default = None)
    latitude = db.Column(db.Float, default = 0.0)
    longitude = db.Column(db.Float, default = 0.0)
    status_id = db.Column(db.Integer, db.ForeignKey('application_status.id'),default=1) 
    applicants_details = db.Column(db.String, default = None)
    media_data = db.Column(db.String, default = None)
    review_date = db.Column(db.Date, default = None)
    start_date = db.Column(db.Date, default = None)
    complete_date = db.Column(db.Date, default = None)
    final_date = db.Column(db.Date, default = None)
    is_moderate = db.Column(db.Boolean, default = False)
    moderator_id = db.Column(db.Integer, db.ForeignKey('users.id'), default = None)
    problem_desc = db.Column(db.String(255), default = False)
    base_rate = db.Column(db.Integer, default = 0)
    source = db.Column(db.String(255), default = 0)
    delete_date = db.Column(db.DateTime, default = None)
    update_date = db.Column(db.DateTime, default = datetime.utcnow)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    views_count = db.Column(db.Integer, default = 0)

    tasks = db.relationship('RequestsModel',backref = db.backref("ancestor", remote_side=id),
                                lazy='dynamic',primaryjoin="RequestsModel.id == RequestsModel.redirect_to_application_id")

    categories = db.relationship('ApplicationCategories', backref='categories_appl',
                                lazy='dynamic',primaryjoin="RequestsModel.id == ApplicationCategories.application_id")

    def __repr__(self):
        return f"<application {self.id}>"


    def rate_calculation(self):

        rate = self.base_rate
        user = self.users_task
        user_profile = user.user_profile
        rate += 10 if user_profile.name is not None else 0
        rate += 20 if user_profile.phone_number is not None else 0
        rate += 50 if user.phone_confirm_date is not None else 0
        rate += 20 if self.longitude is not None and self.latitude is not None else 0
        rate += 5 if self.categories is not None and len(self.categories.all())>0 else 0

        media = json.loads(self.media_data) if self.media_data is not None else None
        #Просчёт рейтинга в зависимости от содержания медиа файлов
        has_image = False
        has_video = False

        if media is not None:
            for i in media:
                if i['type'] == 'IMAGE': has_image = True
                if i['type'] == 'VIDEO': has_video = True

                if has_video and has_image: break

        rate += 20 if has_video else 0
        rate += 20 if has_image else 0

        for i in self.tasks:
            rate+=i.rate_calculation()

        return rate
    
    def json_view(self):

        profile = self.users_task.user_profile
        stored_profile_data = {
            "full_name": profile.name,
            "location":  profile.location,
            "phone": profile.phone_number,
            "rating": profile.rate,
            "email": profile.email

        } if profile is not None else None

        return {
                "id": self.id,
                "parent_request_id": self.redirect_to_application_id,
                "description": self.problem_desc,
                "source": self.source,
                "problem_categories": [
                    _.categories_applic.json_view() for _ in self.categories
                ],
                "location": self.address,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "base_rating": self.base_rate,
                "rating": self.rate_calculation(), #сделать просчёт
                "watch_count": self.views_count,
                "status": self.application_status.title if self.status_id is not None else None,
                "attachments": json.loads(self.media_data),
                "stored_profile_data": stored_profile_data,
                "request_consideration_at": self.review_date,
                "begin_request_execution_at": self.start_date,
                "complete_request_execution_at": self.complete_date,
                "request_status_checked_at": self.final_date,
                "is_moderated": self.is_moderate,
                "moderator_id": self.moderator_id,
                "deleted_at": self.delete_date,
                "created_at": self.create_date,
                "updated_at": self.update_date
            }


class Contractors(db.Model):

    __tablename__ = 'executive_authority'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    mnemomic_name = db.Column(db.String(255))
    description = db.Column(db.String(255), default = None)
    responsible_person = db.Column(db.String(255), default = None)
    image = db.Column(db.String(255), default = None)
    hash_tag = db.Column(db.String(255), default = None)
    contact_phone = db.Column(db.String(255), default = None)
    contact_email = db.Column(db.String(255), default = None)
    contact_email_administration = db.Column(db.String(255), default = None)
    tg_id = db.Column(db.String(255), default = None)
    web_site_link = db.Column(db.String(255), default = None)
    additional_information = db.Column(db.String(255), default = None)
    type = db.Column(db.String(255), default = None)
    work_schedule = db.Column(db.String, default = None)
    is_email_alert = db.Column(db.Boolean, default = False)
    is_sms_alert = db.Column(db.Boolean, default = False)
    is_generate_daily_report = db.Column(db.Boolean, default = False)
    is_visible = db.Column(db.Boolean, default = False)
    delete_date = db.Column(db.DateTime, default = None)
    update_date = db.Column(db.DateTime, default = datetime.utcnow)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    problems = db.relationship('ContractorsProblems', backref='categories_contract', 
                                lazy='dynamic',primaryjoin="Contractors.id == ContractorsProblems.contractor_id")

    def __repr__(self):
        return f"<contractor {self.id}>"


    def json_view(self):

        return {
            "id": self.id,
            "mnemonic_name": self.mnemomic_name,
            "title": self.title,
            "description": self.description,
            "responsible_person": self.responsible_person,
            "image": self.image,
            "hash_tag": self.hash_tag,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "pre_controller_email": self.contact_email_administration,
            "telegram_chat_id": self.tg_id,
            "public_website": self.web_site_link,
            "more_info": self.additional_information,
            "type":self.type,
            "schedule": json.loads(self.work_schedule if self.work_schedule is not None else "[]"),
            "problem_categories": [ _.categories_contracts.json_view() for _ in self.problems ],
            "is_active": self.is_visible,
            "generate_daily_report": self.is_generate_daily_report,
            "need_inform_by_email": self.is_email_alert,
            "need_inform_by_sms": self.is_sms_alert,
            "deleted_at": self.delete_date,
            "created_at": self.create_date,
            "updated_at": self.update_date
        }


class ContractorsProblems(db.Model):

    __tablename__ = 'contractors_problems'

    id = db.Column(db.Integer, primary_key = True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem_categories.id'))
    contractor_id = db.Column(db.Integer, db.ForeignKey('executive_authority.id'))