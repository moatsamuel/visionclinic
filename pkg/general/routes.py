from flask import render_template, request, Blueprint, url_for, redirect, session
from pkg import db
from pkg.models import Doctor, Patient, Specialty
from werkzeug.security import generate_password_hash, check_password_hash



general = Blueprint('general', __name__, template_folder ='templates' )

@general.route("/")
def home():
    if session.get('activeuser') != None:
        doctors = Doctor.query.all()
        doc_email = session.get('activeuser')
        doctor = Doctor.query.filter_by(email=doc_email).first()
        
        return render_template("general/index.html", docs=doctors, doctor=doctor )     
    return redirect(url_for('user.login'))
    
  

@general.route("/viewdoctor/")
def doctors():
    if session.get('activepatient') !=None or session.get('activepatient') != None:
        doctors = Doctor.query.all()
        return render_template("general/doctor.html", doctors=doctors)
    return redirect(url_for('user.home'))

@general.route("/specialties/")
def specialties():
    
    return render_template("general/specialty.html")
    

@general.route("/contact/")
def contact():
    return render_template("general/contact.html")


# @general.route("/register")
# def register():
#     return render_template("general/register.html")


# @general.route("/login")
# def login():
#     return render_template("general/login.html")

   

@general.route("/admin/")
def admin():
   
    return render_template("general/admin.html")
  

@general.route("/document/")
def document():
   
    return render_template("general/document.html")
    return redirect(url_for('user.home'))

@general.route("/medical/")
def medical_record():
    
    return render_template("general/medical-record.html")
    return redirect(url_for('user.home'))

@general.route("/notification/")
def notify():
    
    return render_template("general/notification.html")
    return redirect(url_for('user.home'))

@general.route("/patient/")
def patient():
   
    return render_template("general/patient.html")
    return redirect(url_for('user.home'))

@general.route("/profile/")
def profile():
    if session.get('activepatient') != None or session.get('activeuser') != None :
        return render_template("general/profile.html")

    return redirect(url_for('user.home'))


