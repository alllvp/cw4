from sqlalchemy import Column, String, Integer, Float, ForeignKey

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(100), unique=True, nullable=False)
    description = Column(String, unique=False, nullable=True)
    trailer = Column(String, unique=False, nullable=True)
    year = Column(Integer, unique=False, nullable=True)
    rating = Column(Float, unique=False, nullable=True)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    director_id = Column(Integer, ForeignKey('directors.id'))


class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, unique=False, nullable=False)
    name = Column(String, unique=False, nullable=True)
    surname = Column(String, unique=False, nullable=True)
    favourite_genre = Column(Integer, ForeignKey('genres.id'))


class Bookmark(models.Base):
    __tablename__ = 'bookmarks'

    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
