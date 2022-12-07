import os


class Config:
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_database = os.environ.get("DB_DATABASE")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
