from tinydb import TinyDB, Query, where
from schema.auth_model import UserInDB, Registraion


class DBAccessor:
    EMAIL_COLUMN = "email"
    USERNAME_COLUMN = "username"
    PASSWORD_COLUMN = "password"
    FULLNAME_COLUMN = "full_name"
    HASHED_PASSWORD_COLUMN = "hashed_password"
    DISABLED_COLUMN = "disabled"
    DB_PATH = './db.json'

    def __init__(self) -> None:
        self.db = TinyDB(self.DB_PATH)

    def insert(self, schema):
        self.db.insert(schema)

    def get_email(self, email):
        return self.db.search(where(self.EMAIL_COLUMN) == email)

    def get_user(self, username: str):
        user = self.db.search(where(self.USERNAME_COLUMN) == username)
        # ユーザが存在しなければ空のリストを返す
        return UserInDB(**user[0]) if user else user

    def get_content(self, username: str):
        user = self.db.search(where(self.USERNAME_COLUMN) == username)
        # ユーザが存在しなければ空のリストを返す
        return Registraion(**user[0]) if user else user

    def upsert_content(self, username: str, content):
        self.db.upsert(content.dict(),
                       where(self.USERNAME_COLUMN) == username)
