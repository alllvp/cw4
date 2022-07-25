from flask import abort
from flask_restx import Namespace, Resource

from project.container import bookmark_service, user_service
from project.setup.api.models import bookmark
from project.tools.security import auth_required

api = Namespace('favourites')


@api.route('/movies/<int:movie_id>/')
class BookmarkView(Resource):

    @auth_required
    @api.response(404, 'Not Found')
    def post(self, movie_id):
        """
        Create bookmark by movie id.
        """
        auth_user = user_service.get_user_by_token()
        req_json = {"user_id": auth_user.id, "movie_id": movie_id}
        bookmark_service.create(req_json)
        return "", 201, {"location": f"/favourites/movies/{movie_id}"}

    @auth_required
    @api.response(404, 'Not Found')
    def delete(self, movie_id):
        """
        Delete bookmark by movie id.
        """
        auth_user = user_service.get_user_by_token()
        item_to_del = bookmark_service.get_by_movie_and_user_ids(movie_id, auth_user.id)
        bookmark_service.delete(item_to_del.id)
        return "success", 201, {"location": f"/favourites/movies/{movie_id}"}
