from typing import Optional

from project.dao import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import get_data_from_token


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def create(self, user_d):
        return self.dao.create(user_d)

    def get_filtered(self, username, password):
        return self.dao.get_filtered(username, password)

    def get_user_by_token(self):
        data = get_data_from_token()
        if data:
            return self.dao.get_user_by_login(data.get('email'))

    def partially_update(self, user_d):
        return self.dao.partially_update(user_d)

    def passw_update(self, user_d, password):
        return self.dao.passw_update(user_d, password)
