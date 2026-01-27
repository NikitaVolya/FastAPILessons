from typing import List

from sqlalchemy.orm import Session

from models import UserModel
from repositories.roles import RoleRepository
from repositories.users import UserRepository
from schemas.event import EventRead
from schemas.user import UserCreate, UserRead
from services.roles import RoleService


class UserService:

    def __init__(self, repository: UserRepository):
        self.__repository: UserRepository = repository

    def register(self, db: Session, user: UserCreate) -> UserModel:
        roleService = RoleService(RoleRepository())

        role = roleService.find_role_by_name(db, user.role_name)
        if role is None:
            raise ValueError("Role not found")

        return self.__repository.create(db, first_name=user.first_name, last_name=user.last_name, role_id=role.id)

    def get_user_by_id(self, db: Session, user_id: int) -> UserModel:
        return self.__repository.find_by_id(db, user_id)

    def get_all(self, db) -> List[UserRead]:
        return [UserRead(first_name=user.first_name, last_name=user.last_name, id=user.id, role_name=user.role.name) for user in self.__repository.get_all(db)]
