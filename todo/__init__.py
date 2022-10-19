from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager


db =  SQLAlchemy()
DB_NAME = "tododb.db"
login_manager = LoginManager()


def create_app():
	app = Flask(__name__)
	
	from .app_config import Config
	app.config.from_object(Config)
		
	db.__init__(app)
	from .models import User, Todo
	create_db(app)
	
	from .views import views
	app.register_blueprint(views)
	
	login_manager.__init__(app)
	login_manager.login_view = "views.log_in"
	login_manager.login_message_category = 'info'
	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))
	
	return app

	
def create_db(app):
	if not os.path.exists("todo/" + DB_NAME):
		db.create_all(app=app)
