from typing import Optional
from project.dao import BookmarksDAO
from project.models import Bookmark


class BookmarksService:
    def __init__(self, dao: BookmarksDAO) -> None:
        self.dao = dao

    def get_all(self, page: Optional[int] = None) -> list[Bookmark]:
        return self.dao.get_all(page=page)

    def get_by_movie_and_user_ids(self, movie_id, user_id):
        return self.dao.get_bookmark_by_movie_id_and_user_id(movie_id, user_id)

    def create(self, book_d):
        return self.dao.create(book_d)

    def delete(self, rid):
        self.dao.delete(rid)


