import os 

class GeneralConfig(object):
    APP_NAME = 'VisoinClinic'
    SECRET_KEY = 'notsecured'
    
class DevelopmentConfig(GeneralConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@localhost/visionclinic_db' 
    
    
    