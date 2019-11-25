from flask import render_template, url_for, request, redirect
from app import webapp
from app.utils import awsUtils

awsSuite = awsUtils.AWSSuite()

@webapp.route('/spot/<spotId>')
def viewSpot(spotId):
    spotItem = awsSuite.getSpotById(spotId)
    return render_template('spot.html', spot=spotItem)