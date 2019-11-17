from flask import render_template
from app import webapp

@webapp.route('/')
def home():
    print("hello")
    return render_template('city.html')