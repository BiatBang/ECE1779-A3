from flask import render_template, url_for, request, redirect, session
import json
from app import webapp
from app.utils import awsUtils

awsSuite = awsUtils.AWSSuite()

@webapp.route('/spot/<spotId>')
def viewSpot(spotId):
    userId = session.get('userId') 
    is_login = False
    if session.get('username') is not None:
        is_login = True
        username = session.get('username')
    spotItem = awsSuite.getSpotById(spotId)
    reviews = spotItem['reviews']
    inCart = 0
    if userId:  
        userRating = awsSuite.getUserRating(userId, spotId)
        userReview = awsSuite.getUserReview(userId, spotId)
        userItem = awsSuite.getUserById(userId)
        if spotId in userItem['cart']:
            inCart = 1
    else: 
        userRating = 0
        userReview = ""

    userReview = userReview.replace('\n', '&#10;')
    return render_template('spot.html', spot=spotItem, reviews=reviews, userRating=userRating, userReview=userReview, is_login=is_login, username=username, inCart=inCart)

@webapp.route('/checkPreReview', methods=['POST'])
def checkPreReview():
    userId = 'JVEy3EPgSA'
    spotId = request.json['spotId']
    preReview = awsSuite.checkPreReview(spotId, userId)
    return preReview

@webapp.route('/saveReview', methods=['POST'])
def saveReview():
    # userId = session['userId']
    userId = session.get('userId')
    spotId = request.json['spotId']
    newReview = request.json['newReview']
    starNum = request.json['starNum']
    curRate = request.json['curRate']
    if len(newReview) == 0:
        return json.dumps({'success': 0, 'msg': "No plans in this schedule"})
    else:
        awsSuite.saveRating(spotId, userId, starNum, curRate)
        awsSuite.saveReview(spotId, userId, newReview)
        return json.dumps({'success': 1})
