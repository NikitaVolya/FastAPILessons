from sqlalchemy.orm import Session

from models.departament import DepartamentModel
from repositories.departaments import DepartamentRepository
from schemas.departament import DepartamentCreate


class DepartamentService:

    def __init__(self, repository: DepartamentRepository):
        self.__repository: DepartamentRepository = repository

    def register(self, db: Session, departament: DepartamentCreate) -> DepartamentModel:
        departament_exists = self.__repository.get_departament_by_name(db, departament.name)
        if departament_exists is not None:
            raise ValueError(f"Departament with name \'{departament.name}\' already exists")
        return self.__repository.create(db, name=departament.name, description=departament.description)

    def find_departament_by_id(self, db: Session, departament_id: int = None) -> DepartamentModel:
        departament = self.__repository.get_departament_by_id(db, departament_id)
        if departament is None:
            raise ValueError(f"Departament with id \'{departament_id}\' does not exist")
        return departament

    def find_departament_by_name(self, db: Session, departament_name: str) -> DepartamentModel:
        departament = self.__repository.get_departament_by_name(db, departament_name)
        if departament is None:
            raise ValueError(f"Departament with name \'{departament_name}\' does not exist")
        return departament

    def get_all(self, db: Session) -> list[DepartamentModel]:
        return self.__repository.get_all(db)