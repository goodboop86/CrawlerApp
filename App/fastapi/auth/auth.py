from tinydb import TinyDB, Query
import os

DB_NAME = 'users.json'


class Auth:
    user_table = 'users'
    username_column = "username"
    password_column = "password"

    def __init__(self) -> None:
        self.db = TinyDB(DB_NAME)
        self.users = Query()
        self.useaname = None
        self.password = None

    def signup(self, username, password):
        table = self.db.table(self.user_table)
        self.useaname = username
        self.password = password

        if self._is_already_register():
            return {"status": "error", "message": "already registaerd!"}
        else:
            table.insert({self.username_column: username,
                         self.password_column: password})
            return {"status": "success", "message": "account created!"}

    def login(self, username, password):
        self.useaname = username
        self.password = password

        if self._is_already_register():
            return {"status": "success", "message": "login success!"}
        else:
            return {"status": "error", "message": "account not found!"}

    def _is_already_register(self):
        return self.db.search((self.users.name == self.username) & (self.users.password == self.password))
