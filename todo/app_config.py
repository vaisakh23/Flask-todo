from . import DB_NAME

class Config:
	SECRET_KEY = 'thisisasecretkey'
	SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
	SQLALCHEMY_TRACK_MODIFICATIONS = 'False'