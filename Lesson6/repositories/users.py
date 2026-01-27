from sqlalchemy.orm import Session

from models import UserModel


class UserRepository:

    def create(self, db: Session, first_name: str, last_name: str, role_id: int) -> UserModel | None:
        user = UserModel(first_name=first_name, last_name=last_name, role_id=role_id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def find_by_id(self, db: Session, user_id: int) -> UserModel | None:
        return db.query(UserModel).filter_by(id=user_id).first()

    def get_all(self, db: Session) -> list[UserModel]:
        return db.query(UserModel).all()