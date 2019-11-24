from flask import render_template, session, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

from app.utils.utils import *
from app.utils import awsUtils
from app.forms import RegisterForm, LoginForm
from app import webapp

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
bootstrap = Bootstrap(webapp)
awsSuite = awsUtils.AWSSuite()

@webapp.route('/userPage/<uid>')
def user_page(uid):
    table = dynamodb.Table('user')
    
    # user_Id = qwertyuiopoi
    response = table.get_item(
        Key = {'userId': uid},
        ProjectionExpression = "#name, schedules",
        ExpressionAttributeNames = {"#name": "name"}
    )
    username = response['Item']['name']
    schedules = response['Item']['schedules']
    # print(response['Item'])

    return render_template("userInfo.html", username=username, schedules=schedules)

@webapp.route('/deleteSchedule', methods=['POST'])
def deleteSchedule():
    ###### get userId from session
    userId = "qwertyuiopoi"
    scheduleName = request.json['scheduleName']
    awsSuite.deleteSchedule(userId, scheduleName)
    return json.dumps({'success': 1})