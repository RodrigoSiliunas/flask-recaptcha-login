from app.database import client
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

db = client['captcha']
users_collection = db['users']

blueprint = Blueprint('profile', __name__)


@blueprint.route('/api/auth', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        current_user = get_jwt_identity()
    except:
        return jsonify({
            "error": {
                "message": "Missing Authorization Header.",
                "type": "TokenNotFoundError",
                "code": 401
            }
        }), 401

    valid_user = users_collection.find_one({'email': current_user})

    if not valid_user:
        return jsonify({
            "error": {
                "message": "User not found.",
                "type": "UserExistsError",
                "code": 404
            }
        }), 404

    # Here I remove the fields _id and password from BSON.
    del valid_user['_id'], valid_user['password']

    return jsonify({
        "success": {
            "message": "User successfully found.",
            "profile": valid_user,
            "code": 200
        }
    }), 200
