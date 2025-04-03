class Config:
    SECRET_KEY = 'random string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///groceries.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# sqlite:///relative/path/to/file.db