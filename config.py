import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/music_recommender'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'