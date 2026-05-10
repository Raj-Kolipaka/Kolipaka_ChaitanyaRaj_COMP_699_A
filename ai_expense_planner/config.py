class Config:
    SECRET_KEY = "secret123"

    # SQLite database
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

    SQLALCHEMY_TRACK_MODIFICATIONS = False