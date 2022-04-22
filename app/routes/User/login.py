import hashlib
from datetime import datetime
from app.database import client
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask import Blueprint, request, jsonify

db = client['captcha']
users_collection = db['users']

blueprint = Blueprint('login', __name__)


@blueprint.route('/api/login', methods=['POST'])
def login():
    login_json = request.get_json()
    user_exists = users_collection.find_one({'email': login_json['email']})

    if not user_exists:
        return jsonify({
            "error": {
                "message": "User not exists.",
                "type": "UserExistsError",
                "code": 404
            }
        }), 404

    # Encrypt the password who I recived from JSON.
    password_encrypted = hashlib.sha256(
        login_json['password'].encode('utf8')).hexdigest()

    if (password_encrypted == user_exists['password']):
        json_web_token = create_access_token(identity=login_json['email'])

        user_already_logged_in = users_collection.find_one(
            {'email': login_json['email'], 'token_information': {'$exists': True}})

        if user_already_logged_in is not None:
            users_collection.update_one(
                {'email': login_json['email']},
                {
                    '$set': {
                        'token_information.access_token': json_web_token,
                        'token_information.updated_at': datetime.utcnow().isoformat(' ')
                    }
                })
        else:
            users_collection.update_one(
                {'email': login_json['email']},
                {
                    '$set': {
                        'token_information': {
                            'access_token': json_web_token,
                            'created_at': datetime.utcnow().isoformat(' ')
                        }
                    }
                })

        return jsonify({
            "success": {
                "message": "Your identity has been accepted.",
                "access_token": json_web_token,
                "code": 201
            }
        }), 201

    return jsonify({
        "error": {
            "message": "The username or password is incorrect.",
            "type": "UserExistsError",
            "code": 401
        }
    }), 401
