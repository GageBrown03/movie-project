import os

class DBConfig:
    URI = os.getenv('DATABASE_URL')

class Config:
    DB = DBConfig()

cfg = Config()