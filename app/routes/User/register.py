import hashlib
from app.database import client
from flask import Blueprint, request, jsonify

db = client['captcha']
users_collection = db['users']

blueprint = Blueprint('register', __name__)


@blueprint.route('/api/users', methods=['POST'])
def register():
    new_user = request.get_json()
    user_exists = users_collection.find_one({"email": new_user["email"]})

    if user_exists:
        return jsonify({
            "error": {
                "message": "User already exists.",
                "type": "UserExistsError",
                "code": 409
            }
        }), 409

    new_user['password'] = hashlib.sha256(
        new_user['password'].encode('utf8')).hexdigest()
    users_collection.insert_one(new_user)

    return jsonify({
        "success": {
            "message": "User successfully registered.",
            "code": 201
        }
    }), 201
