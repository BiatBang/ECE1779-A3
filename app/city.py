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
    cityId = "HAjKLj7Ooy"
    return redirect(url_for('viewCity', cityId=cityId))

"""
URL to city page. Displays city image, spots in this city, brief
description of spots.
Listen to "adding cart" button.
"""
@webapp.route('/city/<cityId>', methods=['GET'])
def viewCity(cityId):
    is_login = False
    username = ""
    if not session.get('username'):
        userCart = []
    if session.get('username') is not None:
        is_login = True
        username = session.get('username')
        userId = session.get('userId')
        userCart = awsSuite.getCartByUserId(userId)
    cityItem = awsSuite.getCityById(cityId)
    if not cityItem:
        return render_template('404.html'), 404
    spotIds = cityItem['spots']
    ## retrieve popular spots from "pop" column in city table.
    popSpotIds = cityItem['popSpot']
    popSpots = []
    for i in range(len(popSpotIds)):
        spot = awsSuite.getSpotById(popSpotIds[i])
        if spot and 'name' in spot and len(spot['images']) > 0:
            popSpots.append(spot)
        else:
            for spotId in spotIds:
                if spotId not in popSpotIds:
                    popSpotIds[i] = spotId
                    spot = awsSuite.getSpotById(popSpotIds[i])
                    if spot and 'name' in spot and len(spot['images']) > 0:
                        popSpots.append(spot)
                        break
    ## retrieve recommendations from personalize, handle the conflicts.
    recoms = []
    recomSpots = []
    try:
        recoms = awsSuite.getUserRecommendations(cityId, userId)
        count = 0
        for recom in recoms:
            if count > 1:
                break
            if recom not in popSpotIds:
                recspot = awsSuite.getSpotById(recom)
                recomSpots.append(recspot)
                count += 1
    except:
        print('did not get recommendations')
    spots = []
    for spotId in spotIds:
        spot = awsSuite.getSpotById(spotId)
        if 'name' in spot and len(spot['images']) > 0 and spotId not in popSpotIds and spotId not in recoms:
            spots.append(spot)
    userCartStr = json.dumps(userCart)
    cityImg = urlUtils.getCityS3Url(cityItem['name'])
    return render_template('city.html', cityImg=cityImg, recomSpots=recomSpots, popSpots=popSpots, spots=spots, cityItem=cityItem, userCart=userCart, is_login=is_login, username=username, cityId=cityId)

@webapp.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

"""
A very clumsy way to search city, which doesn't allow cities with the same name.
"""
@webapp.route('/searchCity/<cityName>', methods=['GET', 'POST'])
def searchCity(cityName):
    # a very vague name
    cityLists = None
    cityItem = awsSuite.getCityByName(cityName)
    if cityItem and 'cityId' in cityItem:
        cityId = cityItem['cityId']
    else:
        cityId = "aaaaaaa"
    return redirect(url_for('viewCity', cityId=cityId))

"""
click cart button, go to schedule page
"""
@webapp.route('/gotoCart', methods=['GET'])
def gotoCart():
    if not session.get('username'):
        return redirect(url_for('login'))
    return redirect(url_for('/viewCart'))

"""
When click add button, add it to "cart" column in user table.
"""
@webapp.route('/addSpotToCart', methods=['POST'])
def addSpotToCart():
    if not session.get('username'):
        ## make login remember where it came from
        if request.json['from'] == 'city':
            session['url'] = "viewCity#" + request.json['cityId']
            return json.dumps({'success': 0})
        if request.json['from'] == 'spot':
            session['url'] = "viewSpot#" + request.json['spotId']
            return json.dumps({'success': 0})
    userId = session.get('userId')
    spotId = request.json['spotId']
    awsSuite.addSpotToCart(userId, spotId)
    spotItem = awsSuite.getSpotById(spotId)
    cityId = spotItem['cityId']
    awsSuite.addOneClick(spotId, cityId)
    awsSuite.addUserHabit(userId, spotId)
    return json.dumps({'success': 1})

"""
When you have a click on spot, add it to click table
"""
@webapp.route('/countClick', methods=['POST'])
def countClick():
    spotId = request.json['spotId']
    awsSuite.addOneClick(spotId)