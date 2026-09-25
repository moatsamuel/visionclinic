import os
from flask import Flask
from flask_migrate import Migrate
from pkg.config import DevelopmentConfig
from dotenv import load_dotenv 

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from pkg.general.routes import general
from pkg.doctors.routes import doctor
from pkg.specialty.routes import specialty





def create_app():
    #from pkg.models import db
    
    app = Flask(__name__, static_folder='static')
    app.config.from_object(DevelopmentConfig)
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')

    app.register_blueprint(general)
    app.register_blueprint(doctor)
    app.register_blueprint(specialty)
    

    db.init_app(app)
    
    migrate = Migrate(app, db)
    return app
    
app = create_app()









