# -*- coding: utf-8 -*-


import uvicorn
from crawler.crawler_factory import CrawlerFactory
from fastapi import FastAPI
from datamodel.baseshop_model import Shop, Item
from datamodel.request_model import CrawlRequest, AuthRequest
from typing import Union
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.authenticator import Authenticator, get_current_active_user
from datamodel.auth_model import User, Token, Registraion


app = FastAPI()


@app.post("/oauth2_signup")
def oauth2_signup(request: AuthRequest):
    auth = Authenticator()
    response = auth.oauth2_signup(
        address=request.address, password=request.password)
    return response


@app.post("/oauth2_signin", response_model=Token)
async def oauth2_signin(request: OAuth2PasswordRequestForm = Depends()):
    auth = Authenticator()
    response = auth.oauth2_signin(
        address=request.username, password=request.password)
    return response


@app.get("/users/me/", response_model=User)
async def users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/register", response_model=User)
async def register(current_user: Registraion = Depends(get_current_active_user)):
    return current_user


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
