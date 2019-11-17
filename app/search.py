from flask import render_template, redirect, url_for
from app import webapp
import json

"""
happens when click add button, bring a spotId here
"""
@webapp.route('/addToCart/<spotId>', methods=['GET', 'POST'])
def addToCart(spotId):
    # some actions here
    # here better to use an ajax to call this function
    result = None # 
    return json.dumps({})