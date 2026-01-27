from sqlalchemy.orm import Session

from models import RoleModel
from repositories.roles import RoleRepository
from schemas.role import RoleCreate


class RoleService:

    def __init__(self, repository: RoleRepository):
        self.__repository: RoleRepository = repository

    def create_role(self, db: Session, role_create: RoleCreate) -> RoleModel:
        existing_role = self.__repository.get_by_name(db, role_create.name)
        if existing_role is not None:
            raise ValueError(f"Role {role_create.name} already exists")

        return self.__repository.create(db, name=role_create.name)

    def find_role_by_name(self, db: Session, name: str = None) -> RoleModel:
        role = self.__repository.get_by_name(db, name)
        if role is None:
            raise ValueError(f"Role with name \'{name}\' not found")
        return role

    def find_role_by_id(self, db: Session, id: int) -> RoleModel:
        role = self.__repository.get_by_id(db, id)
        if role is None:
            raise ValueError(f"Role with id \'{id}\' not found")
        return role