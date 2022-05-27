from tinydb import TinyDB, Query, where
import re
import os
import hashlib
from pydantic import SecretStr, EmailStr

DB_PATH = './db.json'


class Auth:
    user_table = 'users'
    address_column = "address"
    password_column = "password"

    def __init__(self) -> None:
        self.db = TinyDB(DB_PATH)
        self.where = Query()
        self.useaname = None
        self.password = None

    def signup(self, address: EmailStr, password: SecretStr):
        self.address = address
        self.password: str = hashlib.sha256(str.encode(
            password.get_secret_value())).hexdigest()

        if self._is_address_exists():
            return {"status": "error", "message": "this mailaddress is already exists ;_;"}
        else:
            self.db.insert({self.address_column: self.address,
                            self.password_column: self.password})
            return {"status": "success", "message": "account created!"}

    def signin(self, address, password):
        self.address = address
        self.password: str = hashlib.sha256(str.encode(
            password.get_secret_value())).hexdigest()

        if not self._is_address_exists():
            return {"status": "error", "message": "mailaddress is not found ;_;"}
        else:
            return self._verify()

    def _is_address_exists(self):
        is_exists = len(self.db.search(
            where(self.address_column) == self.address)) != 0
        return is_exists

    def _verify(self):
        profile = self.db.search(
            (where(self.address_column) == self.address))
        assert len(profile) == 1
        profile = profile[0]

        is_address_correct = re.fullmatch(self.address, profile['address'])
        is_password_correct = re.fullmatch(
            self.password, profile['password'])

        if is_address_correct and is_password_correct:
            return {"status": "success", "message": "login success ^_^"}
        else:
            return {"status": "error", "message": "something wrong ;_;"}
