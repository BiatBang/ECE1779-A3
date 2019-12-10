from flask import render_template, session, flash, redirect, url_for, request
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

from app.utils.utils import *
from app.utils import awsUtils
from app.forms import RegisterForm, LoginForm
from app import webapp

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
awsSuite = awsUtils.AWSSuite()

@webapp.route('/userPage', methods=['GET'])
def userPage():
    if not session.get('username'):
        session['url'] = 'viewCartDefault'
        return redirect(url_for('userPage'))
    if session.get('username') is not None:
        is_login = True
        username = session.get('username')
    userId = session.get('userId')
    userItem = awsSuite.getUserById(userId)
    if not userItem:
        return render_template('404.html'), 404
    else:
        username = userItem['name']
        schedules = userItem['schedules']
    return render_template("userInfo.html", username=username, schedules=schedules, is_login=is_login)

@webapp.route('/deleteSchedule', methods=['POST'])
def deleteSchedule():
    ###### get userId from session
    userId = session.get('userId')
    scheduleName = request.json['scheduleName']
    awsSuite.deleteSchedule(userId, scheduleName)
    return json.dumps({'success': 1})