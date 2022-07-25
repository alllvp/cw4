from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Директор', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Тарантино'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Индиана'),
    'description': fields.String(required=False, example='Фильм о ...'),
    'trailer': fields.String(required=False, example='https://youtube.com/...'),
    'year': fields.Integer(required=False, example=2000),
    'rating': fields.Float(required=False, example=9.1),
    'genre_id': fields.Integer(required=False, example=1),
    'director_id': fields.Integer(required=False, example=1),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=False, max_length=100, example='my@mail.ru'),
    'password': fields.String(required=False, example='secret'),
    'name': fields.String(required=True, example='vasya'),
    'surname': fields.String(required=False, example='Ivanov'),
    'favourite_genre': fields.Integer(required=False, example=1),
})

bookmark: Model = api.model('Избранное', {
    'id': fields.Integer(required=True, example=1),
    'user_id': fields.Integer(required=False, example=1),
    'movie_id': fields.Integer(required=False, example=1),
})
