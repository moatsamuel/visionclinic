from flask import Blueprint, render_template, request,  url_for, redirect, session
from pkg import db
from pkg.models import Patient, User
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint('user', __name__, template_folder='templates', url_prefix='/user')

@user.route("/")
def home():
    return render_template("users/home.html")


@user.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        if email != None and password != None:
            newuser = Patient.query.filter_by(email=email).first()
            
            if newuser and check_password_hash(newuser.password_hash, password):
                session['activepatient'] = newuser.email
                return redirect(url_for('user.dashboard'))
            else:
                return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.login'))
    return render_template('users/login.html')


@user.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_pwd = request.form.get('confirm_pwd')
        
        if not all((fname,lname,email, phone, password, confirm_pwd )):
            return redirect(url_for('user.register'))
        
        u_email = Patient.query.filter_by(email=email).first()
        user_exists = User.query.filter_by(email=email).first()
        if u_email or user_exists:
            return "<h1> Account already exist Please try logging in to your account </h1>"
            
        if password != confirm_pwd:
            return redirect(url_for('user.register'))
        
        user_pwd = generate_password_hash(password)
        nw_user = User(email=email, role='patient', password_hash=user_pwd)
        db.session.add(nw_user)
        db.session.flush()
        
        patient_record = Patient(first_name=fname,last_name=lname, email=email, phone=phone, password_hash=user_pwd, user_id=nw_user.user_id,)
        db.session.add(patient_record)
        db.session.commit()
                
        return redirect(url_for('user.login'))
        
    return render_template('users/register.html')



@user.route("/dashboard/")
def dashboard():
    if session.get('activepatient') != None:
        patients = Patient.query.all()
        patient_email = session.get('activepatient')
        patient = Patient.query.filter_by(email=patient_email).first()
        
        return render_template('users/index.html', user=patient)
    
    return redirect(url_for('user.login'))

@user.route("/logout/")
def logout():
    if session.get('activepatient') != None:
        session.pop('activepatient', None)
        session.clear()
    return redirect(url_for('user.home'))


@user.route("/appointment/")
def book():
    if session.get('activepatient') != None:
        return render_template('users/appointment.html')
    return redirect(url_for('user.login'))

@user.route("/record/")
def medical_record():
    if session.get('activepatient') != None:
        patient_email = session.get('activepatient')
        patient = Patient.query.filter_by(email=patient_email).first()
        return render_template('users/medical-record.html', user=patient)
    return redirect(url_for('user.login'))