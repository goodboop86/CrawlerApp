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
from datamodel.auth_model import User, Token


app = FastAPI()


@app.post("/oauth2_signup")
def oauth2_signup(request: AuthRequest):
    auth = Authenticator()
    response = auth.oauth2_signup(request.address, request.password)
    return response


@app.post("/oauth2_signin", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    auth = Authenticator()
    user = auth.authenticate_user(
        username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=Authenticator.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
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
