from flask import Flask
from app.database import client
from flask_jwt_extended import JWTManager
from app.configuration import DevelopmentConfiguration

from app.routes.User.register import blueprint as register_route
from app.routes.User.login import blueprint as login_route
from app.routes.User.profile import blueprint as user_profile_route
from app.routes.User.logout import blueprint as logout_route

"""
==========================================================================
 ➠ Backend of Activity (https://github.com/RodrigoSiliunas/)
 ➠ Section By: Rodrigo Siliunas (Rô: https://github.com/RodrigoSiliunas)
 ➠ Related system: Core file of Aplication
==========================================================================
"""

app = Flask(__name__)
jwt = JWTManager(app)

"""
    If you wanna change to production configuration.
    Just change the importation of class and update the argument of parameter.
"""
app.config.from_object(DevelopmentConfiguration)


db = client['captcha']
token_blocked = db['token_block']

# Callback function to check if a JWT exists in the database blocklist.
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = token_blocked.find_one({'jti': jti})

    return token is not None


app.register_blueprint(register_route)
app.register_blueprint(login_route)
app.register_blueprint(logout_route)
app.register_blueprint(user_profile_route)
