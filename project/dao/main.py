from typing import Optional, List

from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO, T
from project.models import Genre, Director, Movie, User, Bookmark


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_ordered(self, page: Optional[int] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__).order_by(desc(self.__model__.year))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create(self, user_d):
        ent = self.__model__(**user_d)
        self._db_session.add(ent)
        self._db_session.commit()
        return ent

    def get_filtered(self, username, password):
        t = self._db_session.query(self.__model__)
        return t.filter(self.__model__.email == username, self.__model__.password == password).first()

    def get_user_by_login(self, username):
        t = self._db_session.query(self.__model__)
        return t.filter(self.__model__.email == username).first()

    def update(self, user_d):
        updating_user = self.get_by_id(user_d.get("id"))
        updating_user.email = user_d.get("title")
        updating_user.name = user_d.get("description")
        updating_user.surname = user_d.get("trailer")
        updating_user.favourite_genre = user_d.get("favourite_genre")
        self._db_session.add(updating_user)
        self._db_session.commit()

    def partially_update(self, user_d):
        updating_user = self.get_by_id(user_d.get("id"))
        if "email" in user_d:
            updating_user.email = user_d.get("email")
        if "name" in user_d:
            updating_user.name = user_d.get("name")
        if "surname" in user_d:
            updating_user.surname = user_d.get("surname")
        if "favourite_genre" in user_d:
            updating_user.favourite_genre = user_d.get("favourite_genre")
        self._db_session.add(updating_user)
        self._db_session.commit()

    def passw_update(self, user_d, password):
        user_d.password = password
        self._db_session.add(user_d)
        self._db_session.commit()


class BookmarksDAO(BaseDAO[Bookmark]):
    __model__ = Bookmark

    def get_bookmark_by_movie_id_and_user_id(self, movie_id, user_id):
        t = self._db_session.query(self.__model__)
        return t.filter(self.__model__.movie_id == movie_id, self.__model__.user_id == user_id).first()

    def create(self, book_d):
        ent = self.__model__(**book_d)
        self._db_session.add(ent)
        self._db_session.commit()
        return ent

    def delete(self, rid):
        movie = self.get_by_id(rid)
        self._db_session.delete(movie)
        self._db_session.commit()

