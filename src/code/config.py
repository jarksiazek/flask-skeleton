import os


class Config:
    db_user = os.environ.get("DB_USER")
