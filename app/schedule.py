from flask import render_template
from app import webapp

"""
redirect to this page, retrieve all items in cart.
"""
@webapp.route('/viewCart')
def viewCart():
    return render_template('schedule.html')