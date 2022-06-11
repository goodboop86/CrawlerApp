from audioop import add
from tinydb import TinyDB, Query, where
import re
import os
import hashlib
from pydantic import SecretStr, EmailStr
from schema.request_model import RegisterRequest

DB_PATH = './db.json'


class Registrar:
    user_table = 'users'
    address_column = "address"
    password_column = "password"

    def __init__(self) -> None:
        self.db = TinyDB(DB_PATH)
        self.where = Query()
        self.useaname = None
        self.password = None

    def register(self, request: RegisterRequest):
        self.address = request.address
        self.registration = request.registration

        if self._is_address_exists():
            return self._registrate()

    def _is_address_exists(self):
        res: list[dict] = self.db.search(
            where(self.address_column) == self.address)
        is_exists = len(res) != 0
        assert len(res) == 1
        return is_exists

    def _registrate(self):
        try:
            self.db.upsert(self.registration.dict(),
                           where(self.address_column) == self.address)
            return {"status": "success", "message": "signin success ^_^"}
        except:
            return {"status": "error", "message": "something wrong ;_;"}
