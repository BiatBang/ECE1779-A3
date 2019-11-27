from flask import render_template, redirect, url_for, request, session
from app import webapp
import json
import pickle
from app.utils import awsUtils, urlUtils
from config import clickRecord

awsSuite = awsUtils.AWSSuite()

"""
main page, retrieve a random city(based on you), then
redirect to city path
"""
@webapp.route('/')
def home():
    print("hello")
    cityId = "HAjKLj7Ooy"
    # response = dynamo.scan(FilterExpression=Attr('menu_id').eq(event['menu_id']))
    return redirect(url_for('viewCity', cityId=cityId))

@webapp.route('/city/<cityId>', methods=['GET'])
def viewCity(cityId):
    """
    for the expandable table, I found one possible way
    https://stackoverflow.com/questions/3897396/can-a-table-row-expand-and-close
    all data is needed, and javascript may be needed for expand
    """
    is_login = False
    username = ""
    if not session.get('username'):
        # return redirect(url_for('login'))
        userCart = []
    if session.get('username') is not None:
        is_login = True
        username = session.get('username')
        userId = session.get('userId')
        userCart = awsSuite.getCartByUserId(userId)
    cityItem = awsSuite.getCityById(cityId)
    print(cityItem)
    if not cityItem:
        return render_template('404.html'), 404
    spotIds = cityItem['spots']
    spots = []
    for spotId in spotIds:
        spot = awsSuite.getSpotById(spotId)
        if 'name' in spot and len(spot['images']) > 0:
            spots.append(spot)
    userCartStr = json.dumps(userCart)
    cityImg = urlUtils.getCityS3Url(cityItem['name'])
    print(cityImg)
    return render_template('city.html', cityImg=cityImg, spots=spots, cityItem=cityItem, userCart=userCart, is_login=is_login, username=username)

@webapp.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

"""
for search bar, javascript is also needed if you want a dropdown of results.
https://www.geeksforgeeks.org/search-bar-using-html-css-and-javascript/
this may be helpful.

Or you may want a new page of result page, up to you
"""
@webapp.route('/searchCity/<cityName>', methods=['GET', 'POST'])
def searchCity(cityName):
    # a very vague name
    cityLists = None
    cityItem = awsSuite.getCityByName(cityName)
    if 'cityId' in cityItem:
        cityId = cityItem['cityId']
    else:
        cityId = "CGwWlDtsEM"
    return redirect(url_for('viewCity', cityId=cityId))

"""
click cart button, go to schedule page
"""
@webapp.route('/gotoCart', methods=['GET'])
def gotoCart():
    if not session.get('username'):
        return redirect(url_for('login'))
    return redirect(url_for('/viewCart'))

@webapp.route('/addSpotToCart', methods=['POST'])
def addSpotToCart():
    if not session.get('username'):
        session['url'] = "viewCartDefault"
        return json.dumps({'success': 0})

    ### get userID from session
    userId = session.get('userId')

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