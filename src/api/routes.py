"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, json
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def login_signup():
    data = json.loads(request.data)
    user = User.query.filter_by(name=data["name"], password=data["password"]).first()

    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id }), 200


@api.route('/login', methods=['POST'])
def login_user():
    data = json.loads(request.data)
    user = User.query.filter_by(name=data["name"], password=data["password"]).first()

    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id }), 200


@api.route('/addUser', methods=['POST'])
def new_user():
    body = json.loads(request.data)
    user_model = User(name = body["name"],password= body["password"])
    db.session.add(user_model)
    db.session.commit()
    return jsonify("msj"),200

@api.route('/user', methods=['GET'])
def get_all_user():
    users= User.query.all()
    users_list = list(map(lambda obj: obj.serialize(), users))
    response = {
        "status": "ok",
        "response": users_list
    }
    return jsonify(response)