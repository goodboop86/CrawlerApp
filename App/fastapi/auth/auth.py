from tinydb import TinyDB, Query, where
import re
import os

DB_PATH = './db.json'


class Auth:
    user_table = 'users'
    username_column = "username"
    password_column = "password"

    def __init__(self) -> None:
        self.db = TinyDB(DB_PATH)
        self.where = Query()
        self.useaname = None
        self.password = None

    def signup(self, username, password):
        self.username = username
        self.password = password

        if self._is_username_exists():
            return {"status": "error", "message": "this mailaddress is already exists ;_;"}
        else:
            self.db.insert({self.username_column: username,
                            self.password_column: password})
            return {"status": "success", "message": "account created!"}

    def signin(self, username, password):
        self.username = username
        self.password = password

        if not self._is_username_exists():
            return {"status": "error", "message": "mailaddress is not found ;_;"}
        else:
            return self._verify()

    def _is_username_exists(self):
        is_exists = len(self.db.search(
            where(self.username_column) == self.username)) != 0
        return is_exists

    def _verify(self):
        profile = self.db.search(
            (where(self.username_column) == self.username))
        assert len(profile) == 1
        profile = profile[0]

        is_username_correct = re.fullmatch(self.username, profile['username'])
        is_password_correct = re.fullmatch(self.password, profile['password'])

        if is_username_correct and is_password_correct:
            return {"status": "success", "message": "login success ^_^"}
        else:
            return {"status": "error", "message": "something wrong ;_;"}
