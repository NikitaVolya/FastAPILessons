from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import DepartamentModel


class DepartamentRepository(BaseModel):

    def create(self, db: Session, name: str, description: str = "") -> DepartamentModel:

        departament = DepartamentModel(
            name=name,
            description=description
        )

        db.add(departament)
        db.commit()
        db.refresh(departament)
        return departament

    def get_departament_by_id(self, db: Session, id: int) -> DepartamentModel | None:
        return db.query(DepartamentModel).filter_by(id=id).first()

    def get_departament_by_name(self, db: Session, name: str) -> DepartamentModel | None:
        return db.query(DepartamentModel).filter_by(name=name).first()

    def get_all(self, db: Session) -> list[DepartamentModel]:
        return db.query(DepartamentModel).all()