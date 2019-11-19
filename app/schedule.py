from flask import render_template, request
from app import webapp
from app.utils import awsUtils
import json

awsSuite = awsUtils.AWSSuite()

"""
redirect to this page, retrieve all items in cart.
"""
@webapp.route('/viewCart')
def viewCart():    
    # for now, after userId should come from 
    userId = "qwertyuiopoi"   
    userItem = awsSuite.getUserById(userId)
    cartItems = userItem['cart']
    scheduleItems = awsSuite.getSchedules(userId)
    spots = []
    for cartItem in cartItems:
        spots.append(awsSuite.getSpotById(cartItem))

    return render_template('schedule.html', userItem=userItem, spots=spots, scheduleItems=scheduleItems)

@webapp.route('/addSpotToSchedule', methods=['GET','POST'])
def addSpotToSchedule():
    spotId = request.json['spotId']
    date = request.json['date']
    startTime = request.json['startTime']
    endTime = request.json['endTime']
    scheduleName = request.json['scheduleName']
    print("into addspot, spotId:", spotId)

    spotItem = awsSuite.getSpotById(spotId)

    return json.dumps(spotItem)