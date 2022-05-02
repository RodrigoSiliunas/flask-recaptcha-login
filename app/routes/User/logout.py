from datetime import datetime
from app.database import client
from flask_jwt_extended import jwt_required, get_jwt
from flask import Blueprint, jsonify

db = client['captcha']
token_blocked = db['token_block']

blueprint = Blueprint('logout', __name__)


@blueprint.route('/api/logout', methods=['DELETE'])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]

    token_blocked.insert_one(
        {'jti': jti, 'created_at': datetime.utcnow().isoformat(' ')})

    return jsonify({
        "success": {
            "message": "You have been successfully logout.",
            "code": 200
        }
    }), 200
