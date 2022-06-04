from passlib.context import CryptContext
from datamodel.auth_model import UserInDB


class Authenticator:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self) -> None:
        pass

    @classmethod
    def authenticate_user(cls, fake_db, username: str, password: str):
        user = cls.get_user(fake_db, username)
        if not user:
            return False
        if not cls.verify_password(password, user.hashed_password):
            return False
        return user

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)

    @staticmethod
    def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)
