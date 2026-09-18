from flask import render_template, request
from pkg import app

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/doctor")
def doctors():
    return render_template("doctor.html")

@app.route("/specialty")
def specialties():
    return render_template("specialty.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/appointment")
def appointment():
    return render_template("appointment.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/document")
def document():
    return render_template("document.html")

@app.route("/medical")
def medical_record():
    return render_template("medical-record.html")

@app.route("/notification")
def notify():
    return render_template("notification.html")

@app.route("/patient")
def patient():
    return render_template("patient.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")


