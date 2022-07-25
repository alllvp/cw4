from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user
from project.tools.security import auth_required, get_hash, create_acc_token, create_refr_token

api = Namespace('user')


@api.route('/')
class UserView(Resource):

    @auth_required
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def get(self):
        """
        Get user profile.
        """
        found_user = user_service.get_user_by_token()
        found_user.password = 'не скажу'
        return found_user

    @auth_required
    def patch(self):
        req_json = request.json
        auth_user = user_service.get_user_by_token()
        req_json["id"] = auth_user.id
        user_service.partially_update(req_json)
        return "", 204


@api.route('/password/')
class PassView(Resource):

    @auth_required
    def put(self):
        req_json = request.json
        auth_user = user_service.get_user_by_token()
        password_1_hash = get_hash(req_json.get('password_1'))
        if password_1_hash != auth_user.password:
            return {"error": "Неверные учётные данные"}, 401
        else:
            user_service.passw_update(auth_user, get_hash(req_json.get('password_2')))

            data = {'email': auth_user.email}
            return {'access_token': create_acc_token(data), 'refresh_token': create_refr_token(data)}, 201
