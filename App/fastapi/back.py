# -*- coding: utf-8 -*-


import uvicorn
from pydantic import BaseModel, Field, HttpUrl, validator, SecretStr, EmailStr
from crawler.crawler_factory import CrawlerFactory
from fastapi import FastAPI
from datamodel.baseshop_model import Shop, Item
from datamodel.request_model import CrawlRequest, AuthRequest, AccuontRequest, RegisterRequest
from typing import Union
from auth.auth import Auth
from register.registrar import Registrar
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from auth.authenticator import Authenticator
from datamodel.auth_model import User, Token, TokenData, UserInDB

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


app = FastAPI()


async def get_current_active_user(current_user: User = Depends(Authenticator.get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    auth = Authenticator()
    user = auth.authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/crawl", response_model=Union[Item, Shop])
def crawl(request: CrawlRequest):
    crawler = CrawlerFactory(request=request)
    result = crawler()
    return result


@app.post("/signup")
def signup(request: AuthRequest):
    auth = Auth()
    response = auth.signup(request.address, request.password)
    return response


@app.post("/signin",)
def signin(request: AuthRequest):
    auth = Auth()
    response = auth.signin(request.address, request.password)
    return response


@app.post("/account",)
def account(request: AccuontRequest):
    auth = Auth()
    response = auth.account(request.address)
    return response


@app.post("/register",)
def register(request: RegisterRequest):
    registrar = Registrar()
    response = registrar.register(request)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
