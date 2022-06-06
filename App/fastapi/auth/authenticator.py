from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Union
from pydantic import SecretStr, EmailStr
from auth.db_accessor import DBAccessor
from fastapi import Depends, HTTPException, status
from datamodel.auth_model import User, TokenData
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Authenticator.SECRET_KEY,
                             algorithms=[Authenticator.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    db = DBAccessor()
    user = db.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class Authenticator:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM = "HS256"
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    def __init__(self) -> None:
        pass

    @classmethod
    def oauth2_signup(cls, address: EmailStr, password: SecretStr):
        password_: str = cls.pwd_context.encrypt(password.get_secret_value())

        db = DBAccessor()
        if db.get_email(address):
            return {"status": "error", "message": "this mailaddress is already exists ;_;"}
        else:
            schema = {
                db.USERNAME_COLUMN: address,
                db.FULLNAME_COLUMN: address,
                db.EMAIL_COLUMN: address,
                db.HASHED_PASSWORD_COLUMN: password_,
                db.DISABLED_COLUMN: False,
            }
            db.insert(schema)
            return {"status": "success", "message": "account created!"}

    @classmethod
    def authenticate_user(cls, username: str, password: str):
        db = DBAccessor()
        user = db.get_user(username=username)
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
