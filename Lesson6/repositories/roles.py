from sqlalchemy.orm import Session

from models import RoleModel


class RoleRepository:

    def create(self, db: Session, name: str) -> RoleModel:

        role = RoleModel(name=name)

        db.add(role)
        db.commit()
        db.refresh(role)

        return role

    def get_by_name(self, db: Session, name: str) -> RoleModel | None:
        return db.query(RoleModel).filter_by(name=name).first()

    def get_by_id(self, db: Session, id: int) -> RoleModel | None:
        return db.query(RoleModel).filter_by(id=id).first()