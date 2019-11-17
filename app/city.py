from flask import render_template, redirect, url_for
from app import webapp
import json

"""
main page, retrieve a random city(based on you), then
redirect to city path
"""
@webapp.route('/')
def home():
    print("hello")
    cityId = 123123
    return redirect(url_for('viewCity', cityId=cityId))

@webapp.route('/city/<cityId>', methods=['GET'])
def viewCity(cityId):
    """
    for the expandable table, I found one possible way
    https://stackoverflow.com/questions/3897396/can-a-table-row-expand-and-close
    all data is needed, and javascript may be needed for expand
    """
    return render_template('city.html', cityId=cityId)

"""
for search bar, javascript is also needed if you want a dropdown of results.
https://www.geeksforgeeks.org/search-bar-using-html-css-and-javascript/
this may be helpful.

Or you may want a new page of result page, up to you
"""
@webapp.route('/search/<cityName>', methods=['GET', 'POST'])
def search(cityName):
    # a very vague name
    cityLists = None #searchCity()
    #return render_template()

"""
happens when click add button, bring a spotId here
"""
@webapp.route('/addToCart/<spotId>', methods=['GET', 'POST'])
def addToCart(spotId):
    # some actions here
    # here better to use an ajax to call this function
    result = None # 
    return json.dumps({})

"""
click cart button, go to schedule page
"""
@webapp.route('/gotoCart', methods=['GET'])
def gotoCart():
    return redirect(url_for('/viewCart'))