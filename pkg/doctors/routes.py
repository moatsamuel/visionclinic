from flask import Blueprint, render_template, request, url_for, redirect, session
from pkg import db
from pkg.models import Specialty, Doctor, User
from werkzeug.security import generate_password_hash, check_password_hash

doctor = Blueprint('doctors', __name__, template_folder='templates', static_folder='static', url_prefix='/doctor' )

@doctor.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("doc_email")
        password = request.form.get("doc_password")
        if email != None and password != None:
            doctor = Doctor.query.filter_by(email=email).first()
            
            if doctor and check_password_hash(doctor.password_hash, password):
                session['activeuser'] = doctor.email    #doctor that is logged in
                return redirect(url_for("doctors.dashboard"))
            else:
                return redirect(url_for("doctors.login"))
        else:
            return redirect(url_for('general.login'))
    return render_template("doctors/login.html")


@doctor.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        specialty_id = request.form.get("specialty_id")
        availability = request.form.get("Availability")
        licence_number = request.form.get("licence_number")
        password = request.form.get("password")
        confirm_pwd = request.form.get("cpassword")
        if not all((first_name, last_name, email, phone, specialty_id, availability, licence_number, password, confirm_pwd)):
            return redirect(url_for('doctors.register'))

        d_email = Doctor.query.filter_by(email=email).first()
        d_licence = Doctor.query.filter_by(licence_number=licence_number).first()
        account_exists = User.query.filter_by(email=email).first()
        if d_email or d_licence or account_exists:
            return "<h1> Doctor Record already exist Contact admin for login information. </h1>"

        if password != confirm_pwd:
            return redirect(url_for('doctors.register'))

        doc_pass = generate_password_hash(password)
        account = User(email=email, role="doctor", password_hash=doc_pass)
        db.session.add(account)
        db.session.flush()

        doctor_record = Doctor(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            specialty_id=specialty_id,
            availability=availability,
            licence_number=licence_number,
            password_hash=doc_pass,
            user_id=account.user_id,
        )
        db.session.add(doctor_record)
        db.session.commit()

        return redirect(url_for("doctors.login"))

    return render_template("doctors/register.html")

@doctor.route("/dashboard")
def dashboard():
    if session.get('activeuser') != None:
        doctors = Doctor.query.all()
        doc_email = session.get('activeuser')
        doctor = Doctor.query.filter_by(email=doc_email).first()
        
        
        return render_template("doctors/doctor.html", doctors=doctors, doc=doctor )
    
    return redirect(url_for('doctors.login'))

@doctor.route("/logout/")
def logout():
    if session.get('activeuser') != None:
        session.pop('activeuser', None)
        session.clear()
    return redirect(url_for('doctors.login'))