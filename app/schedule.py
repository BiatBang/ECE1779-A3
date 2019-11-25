from flask import render_template, request, redirect, url_for, session
from app import webapp
from app.utils import awsUtils
import json

awsSuite = awsUtils.AWSSuite()

@webapp.route('/viewCart')
def viewCartDefault():
    return redirect(url_for('viewCart', scheduleName='New Schedule'))

"""
redirect to this page, retrieve all items in cart.
"""
@webapp.route('/viewCart/<scheduleName>')
def viewCart(scheduleName):    
    # for now, after userId should come from session
    userId = session.get('userId')

    is_login = False
    username = ""
    if not session.get('username'):
        return redirect(url_for('login'))
    if session.get('username') is not None:
        is_login = True
        username = session.get('username')

    userItem = awsSuite.getUserById(userId)
    cartItems = userItem['cart']
    scheduleItems = awsSuite.getSchedules(userId)
    spots = []
    for cartItem in cartItems:
        spots.append(awsSuite.getSpotById(cartItem))
    slots = []
    if scheduleName != "New Schedule":
        slots = awsSuite.getSlotsFromScheduleName(userId, scheduleName)
    if not scheduleName:
        scheduleName = "New Schedule"
    slotsStr = json.dumps(slots).replace('\'', '&#39;')
    # scheduleStr = json.dumps(scheduleItems).replace('\'', '&#39;')
    return render_template('schedule.html',scheduleName=scheduleName, userItem=userItem, spots=spots, scheduleItems=scheduleItems, slots=slotsStr, is_login=is_login, username=username)

"""
happens when click "add" in cart. Remove it from cart. Add it into schedule(in js).
"""
@webapp.route('/addSpotToSchedule', methods=['GET','POST'])
def addSpotToSchedule():
    ###### get userId from session
    userId = session.get('userId')

    spotId = request.json['spotId']
    date = request.json['date']
    startTime = request.json['startTime']
    endTime = request.json['endTime']
    scheduleName = request.json['scheduleName']

    spotItem = awsSuite.getSpotById(spotId)
    spotJson = {
        'spotId': spotItem['spotId'],
        'name': spotItem['name'],
        'location': spotItem['location']
    }
    # remove it from cart
    awsSuite.removeSpotFromCart(userId, spotId)
    return json.dumps(spotJson)

"""
happens when click delete icon
"""
@webapp.route('/removeSpotFromCart', methods=['POST'])
def removeSpotFromCart():
    ###### get userId from session
    userId = session.get('userId')
    spotId = request.json['spotId']
    awsSuite.removeSpotFromCart(userId, spotId)
    return json.dumps({'success': 1})

"""
happens when click save in modal. Collect all from appointments and refresh
or create the schedule
"""
@webapp.route('/saveSchedule', methods=['POST'])
def saveSchedule():
    ###### get userId from session
    userId = session.get('userId')
    scheduleName = request.json['scheduleName']
    spotSlots = request.json['spotSlots']
    isNewSchedule = request.json['isNewSchedule']
    if not spotSlots:
        return json.dumps({'success': 0, 'msg': "No plans in this schedule"})
    saveResult = awsSuite.saveSchedule(userId, scheduleName, spotSlots, isNewSchedule)
    if saveResult == awsUtils.SCHEDULEEXISTED:
        return json.dumps({'success': 2, 'msg': "Schedule name existed"})
    return json.dumps({'success': 1})