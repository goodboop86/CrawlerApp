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

app = FastAPI()


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
