from flask import render_template, redirect, url_for, request
from app import webapp
import json
import pickle
from app.utils import awsUtils
from config import clickRecord

awsSuite = awsUtils.AWSSuite()

"""
main page, retrieve a random city(based on you), then
redirect to city path
"""
@webapp.route('/')
def home():
    print("hello")
    cityId = "CGwWlDtsEM"
    # response = dynamo.scan(FilterExpression=Attr('menu_id').eq(event['menu_id']))
    return redirect(url_for('viewCity', cityId=cityId))

@webapp.route('/city/<cityId>', methods=['GET'])
def viewCity(cityId):
    """
    for the expandable table, I found one possible way
    https://stackoverflow.com/questions/3897396/can-a-table-row-expand-and-close
    all data is needed, and javascript may be needed for expand
    """

    ###### get userId from session
    userId = "qwertyuiopoi"

    userCart = awsSuite.getCartByUserId(userId)

    cityItem = awsSuite.getCityById(cityId)
    spotIds = cityItem['spots']
    spots = []
    for spotId in spotIds:
        spot = awsSuite.getSpotById(spotId)
        spots.append(spot)
    userCartStr = json.dumps(userCart)
    return render_template('city.html', spots=spots, cityItem=cityItem, userCart=userCart)

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
click cart button, go to schedule page
"""
@webapp.route('/gotoCart', methods=['GET'])
def gotoCart():
    return redirect(url_for('/viewCart'))

@webapp.route('/addSpotToCart', methods=['POST'])
def addSpotToCart():
    ### get userID from session
    userId = "123123"

    spotId = request.json['spotId']
    print("add into cart:", spotId)
    awsSuite.addSpotToCart(userId, spotId)
    return json.dumps({'success': 1})

@webapp.route('/countClick', methods=['POST'])
def countClick():
    spotId = request.json['spotId']
    # with open(clickRecord, 'a') as f:
    #     f.write(spotId + '\n')
    awsSuite.addOneClick(spotId)