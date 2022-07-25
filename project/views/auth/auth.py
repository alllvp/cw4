import jwt
from flask import request, abort, current_app
from flask_restx import Namespace, Resource

from project.container import user_service
from project.tools.security import get_hash, create_acc_token, create_refr_token

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):

    @api.response(404, 'Not Found')
    def post(self):
        req_json = request.json
        if 'email' in req_json and 'password' in req_json:
            req_json['password'] = get_hash(req_json['password'])
            new_user = user_service.create(req_json)
            return "", 201, {"location": f"/users/{new_user.id}"}
        else:
            return 'Не хватает исходных данных', 200


@api.route('/login')
class AuthsView(Resource):

    @api.response(404, 'Not Found')
    def post(self):
        data = request.json
        if 'email' not in data or 'password' not in data:
            return {"error": "Неверные учётные данные"}, 401
        current_user = user_service.get_filtered(data['email'], get_hash(data['password']))
        if not current_user:
            return {"error": "Неверные учётные данные"}, 401
        data = {"email": current_user.email}
        return {'access_token': create_acc_token(data), 'refresh_token': create_refr_token(data)}, 201, {"location": f"/auth/{current_user.id}"}

    def put(self):
        data = request.json
        if 'refresh_token' not in data:
            return {"error": "Неверные учётные данные"}, 400
        try:
            token = jwt.decode(data['refresh_token'].split('Bearer ')[-1], key=current_app.config['SECRET_KEY'], algorithms=current_app.config['ALGORITHM'])
        except Exception as e:
            abort(401)

        data = {'email': token['email']}
        return {'access_token': create_acc_token(data), 'refresh_token': create_refr_token(data)}, 201
