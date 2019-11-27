from flask import render_template, url_for, request, redirect, session
import json
from app import webapp
from app.utils import awsUtils

awsSuite = awsUtils.AWSSuite()

@webapp.route('/spot/<spotId>')
def viewSpot(spotId):
    # userId = session.get(userId) 
    userId = 'JVEy3EPgSA' # ------------------------

    spotItem = awsSuite.getSpotById(spotId)
    reviews = spotItem['reviews']

    if userId is not None:  
        userRating = awsSuite.getUserRating(userId, spotId)
        userReview = awsSuite.getUserReview(userId, spotId)
    else: 
        userRating = 0
        userReview = ""
    # print(spotItem['images'])
    return render_template('spot.html', spot=spotItem, reviews=reviews, userRating=userRating, userReview=userReview)

@webapp.route('/saveRating', methods=['POST'])
def saveRating():
    # userId = session['userId']
    userId = 'JVEy3EPgSA' # ------------------------
    spotId = request.json['spotId']
    starNum = request.json['starNum']
    curRate = request.json['curRate']
    awsSuite.saveRating(spotId, userId, starNum, curRate)
    return json.dumps({'success': 1})

@webapp.route('/checkPreReview', methods=['POST'])
def checkPreReview():
    userId = 'JVEy3EPgSA'
    spotId = request.json['spotId']
    preReview = awsSuite.checkPreReview(spotId, userId)
    return preReview

@webapp.route('/saveReview', methods=['POST'])
def saveReview():
    # userId = session['userId']
    userId = 'JVEy3EPgSA' # ------------------------
    spotId = request.json['spotId']
    newReview = request.json['newReview']
    if len(newReview) == 0:
        return json.dumps({'success': 0, 'msg': "No plans in this schedule"})
    else:
        awsSuite.saveReview(spotId, userId, newReview)
        return json.dumps({'success': 1})
