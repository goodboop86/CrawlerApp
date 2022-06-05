from passlib.context import CryptContext
from datamodel.auth_model import UserInDB, Token, TokenData
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from pydantic import SecretStr, EmailStr
from tinydb import TinyDB, Query, where

DB_PATH = './db.json'


class Authenticator:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM = "HS256"
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    user_table = 'users'
    address_column = "email"
    username_column = "username"
    password_column = "password"
    fullname_column = "full_name"
    hashed_password_column = "hashed_password"
    db = TinyDB(DB_PATH)

    def __init__(self) -> None:
        self.useaname = None
        self.password = None

    def oauth2_signup(self, address: EmailStr, password: SecretStr):
        self.address = address
        self.password: str = self.pwd_context.encrypt(
            password.get_secret_value())

        if self._is_address_exists():
            return {"status": "error", "message": "this mailaddress is already exists ;_;"}
        else:
            schema = {
                self.username_column: self.address,
                self.fullname_column: self.address,
                self.address_column: self.address,
                self.hashed_password_column: self.password,
                "disabled": False,
            }
            self.db.insert(schema)
            return {"status": "success", "message": "account created!"}

    def _is_address_exists(self):
        is_exists = len(self.db.search(
            where(self.address_column) == self.address)) != 0
        return is_exists

    @classmethod
    def get_user(cls, username: str, db=None):
        user = cls.db.search(where(cls.username_column) == username)
        if user:
            assert len(user) == 1
            return UserInDB(**user[0])

    @classmethod
    def authenticate_user(cls, fake_db, username: str, password: str):
        user = cls.get_user(db=fake_db, username=username)
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

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt
