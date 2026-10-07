from pkg import db
from datetime import datetime




class Specialty(db.Model):
    __tablemname__="specialty"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    name = db.Column(db.Enum("ophthalmology", "optometry", "pediatric eye care", "glaucoma", "cataract care", "eye surgery"), index=True)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    doctors = db.relationship('Doctor', backref="specialties", cascade="all, delete-orphan")
    
    
class User(db.Model):
    __tablename__='users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    email = db.Column(db.String(255), nullable=False ,unique=True)
    role = db.Column(db.Enum("doctor", "patient", "admin", default="patient") )
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    
    user_doctor = db.relationship('Doctor', backref='user', cascade='all, delete-orphan')

    user_patient = db.relationship('Patient', backref='user', cascade='all, delete-orphan')
    

class Patient(db.Model):
    __tablename__='patients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    first_name = db.Column(db.String(200), nullable=False, index=True )
    last_name = db.Column(db.String(200), nullable=False )
    email = db.Column(db.String(255), nullable=False ,unique=True)
    phone = db.Column(db.String(50), nullable=False )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True )
        
   

class Doctor(db.Model):
    __tablename__="doctors"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200), nullable=False, index=True )
    last_name = db.Column(db.String(200), nullable=False )
    email = db.Column(db.String(255), nullable=False ,unique=True)
    phone = db.Column(db.String(50), nullable=False )
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'), unique=False, nullable=False )
    availability = db.Column(db.Enum("available", "unavailable", default="available") )
    licence_number = db.Column(db.String(255), nullable=False )
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True )
    
   
    
    
    def __repr__ (self):
        return f"{self.first_name} - {self.last_name}"
    
    
class Appointment(db.Model):
    __tablename__='appointments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    patient_id = db.Column(db.Integer )
    doctor_id = db.Column(db.Integer )
    appointment_date = db.Column(db.DateTime)
    appointment_time = db.Column(db.DateTime)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum("pending", "accepted", "rejected", "cancelled", "completed", default="pending") )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    


    
    

    
    