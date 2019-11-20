from flask import render_template, session, flash, redirect, url_for
from flask_bootstrap import Bootstrap
import boto3
from boto3.dynamodb.conditions import Key, Attr

from app import webapp

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
bootstrap = Bootstrap(webapp)

@webapp.route('/user_page')
def user_page():
    table = dynamodb.Table('user')

    # userId = session.get('userId')
    # if userId is None:
    #     flash('Please log in first.')
    #     return redirect(url_for('login'))
    # else:
    is_login = True
    userId = '100010'
    response = table.get_item(
        Key = {'userId': userId},
        ProjectionExpression = "schedules"
    )

    schedules = response['Item']['schedules']
    print(response['Item'])

    return render_template("userInfo.html", is_login=is_login, schedules=schedules)

