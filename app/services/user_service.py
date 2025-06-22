# app/services/user_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.security import get_password_hash, verify_password # Import security functions

class UserService:
    def get_user(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            password=hashed_password,
            name=user_in.name # Include name if present
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate_user(self, db: Session, email: str, password: str) -> User | None:
        user = self.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password):
            return None
        return user

    def update_user(self, db: Session, db_user: User, user_in: UserUpdate) -> User:
        update_data = user_in.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            db_user.password = get_password_hash(update_data["password"])
            del update_data["password"]

        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int) -> bool:
        user = self.get_user(db, user_id=user_id)
        if user:
            db.delete(user)
            db.commit()
            return True
        return False

user_service_instance = UserService() # Instantiate for use in routers