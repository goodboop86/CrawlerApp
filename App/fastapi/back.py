# -*- coding: utf-8 -*-

import uvicorn
from crawler.crawler_factory import CrawlerFactory
from schema.baseshop_model import Shop, Item
from schema.request_model import CrawlRequest, AuthRequest
from typing import Union
from datetime import timedelta


from schema.auth_model import User, Token, Registraion
from auth.authenticator import Authenticator, oauth2_scheme, get_current_active_user, register_user_setting, get_current_content
from auth.db_accessor import DBAccessor
from fastapi import Depends, Header, Body
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import FastAPI
app = FastAPI()


@app.post("/oauth2_signup")
async def oauth2_signup(request: AuthRequest):
    auth = Authenticator()
    response = auth.oauth2_signup(
        username=request.username, password=request.password)
    return response


@app.post("/oauth2_signin", response_model=Token)
async def oauth2_signin(request: OAuth2PasswordRequestForm = Depends()):
    auth = Authenticator()
    response = auth.oauth2_signin(
        username=request.username, password=request.password)
    return response


@app.get("/users/me/", response_model=User)
async def users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/account_info")
async def users_me(current_user: User = Depends(get_current_active_user), current_content: Registraion = Depends(get_current_content)):
    return dict(current_user.dict(), **current_content.dict())


@app.post("/register")
async def register(response=Depends(register_user_setting)):
    return response


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/crawl", response_model=Union[Item, Shop])
def crawl(request: CrawlRequest):
    crawler = CrawlerFactory(request=request)
    result = crawler()
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
