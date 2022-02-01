from flask import jsonify, request,send_file
from flask_jwt_extended import get_jwt_identity,jwt_required
from . import routes
from models import Roles
from api import db,app
from datetime import datetime
import errors_response
from geopy.geocoders import Nominatim
from functools import partial
import os

geolocator = Nominatim(user_agent="address_getter")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@routes.route('/services/address', methods=['POST'])
def get_address_route():

    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')

    if longitude is None or latitude is None:
        return jsonify(errors_response.incorrect_data),400
    
    if  type(longitude) != int and type(longitude) != float and not (type(longitude)==str and longitude.isdigit()):
        return jsonify(errors_response.incorrect_data),400
    
    if type(latitude) != int and type(latitude) != float and not (type(latitude)==str and latitude.isdigit()):
        return jsonify(errors_response.incorrect_data),400

    reverse = partial(geolocator.reverse, language="ru")
    location = reverse(f"{latitude}, {longitude}")
    return jsonify({
        'address':location.address
    }),200


def get_address(latitude, longitude):

    reverse = partial(geolocator.reverse, language="ru")
    location = reverse(f"{latitude}, {longitude}")
    return location.address


@routes.route('/services/coords', methods=['POST'])
def get_coords():

    address = request.json.get('address')

    if address is not None and type(address)!=str:
        return errors_response.incorrect_data

    geocode = partial(geolocator.geocode, language="ru")
    location = geocode(address)
    if location is None:
        return jsonify(errors_response.non_existent_record),200
    return jsonify({
        'latitude':location.latitude,
        'longitude' : location.longitude
    }),200


@routes.route('/media/<name>', methods=['GET'])
def get_media(name):

    try:
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        if name:
            return send_file(path)

        return errors_response.non_existent_record

    except:
        return errors_response.non_existent_record

