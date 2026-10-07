from flask import Blueprint, render_template, request, url_for, redirect
from pkg import db
from pkg.models import Specialty, Doctor
#from pkg import app


specialty = Blueprint('specialty', __name__,template_folder="templates", static_folder='static', url_prefix='/specialty' )

@specialty.route('/')
def main():
    specialty_name= input("Enter the specialty name: ")
    specialty_description = input("Enter the specialty description: ") 
    special = Specialty(name=specialty_name, description=specialty_description)
    
    db.session.add(special)
    db.session.commit()
    
    
    return "<h1>  Add Specialty </h1>"

@specialty.route('/update')
def update():
    pass