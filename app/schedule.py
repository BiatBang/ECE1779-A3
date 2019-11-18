from flask import render_template, request
from app import webapp
from app.utils import awsUtils

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
    spots = []
    for cartItem in cartItems:
        print(cartItem)
        spots.append(awsSuite.getSpotById(cartItem))
    print(spots)

    return render_template('schedule.html', userItem=userItem, spots=spots)

@webapp.route('/addSpotToSchedule', methods=['POST'])
def addSpotToSchedule():
    date = request.form['date']
    startTime = request.form['startTime']
    endTime = request.form['endTime']
    print(date, startTime, endTime)
    return ('', 204)