from __future__ import print_function  # Python 2/3 compatibility
from flask import render_template, request, url_for, redirect, flash, session
from app.forms import RegisterForm, LoginForm, SearchForm
from app.utils import stringUtils
from app import webapp

import boto3
from botocore.exceptions import ClientError
import json
from boto3.dynamodb.conditions import Key, Attr
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(webapp)

@webapp.route('/index')
def index():
    form = SearchForm()
    City = request.form.get('search')
    print("hellloooooooooooooo", City)
    # 1. Connect to DB
    # 2. Check username is used or not
    # 3. Insert to DB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    #  client = boto3.Session(region_name='us-east-1', profile_name='dev').client('dynamodb')
    table = dynamodb.Table('city')
    print("hi", table)
    response = table.scan(FilterExpression=Key('name').eq(City))
    print(response)

    is_login = False
    username = ""
    if session.get('username') is not None:
        is_login = True
        username = session.get('username')
    return render_template('base.html',
                           is_login=is_login,
                           username=username,
                           form=form)


@webapp.route('/search')
def search():
    form = SearchForm()

    City = request.form.get('search')
    print("hellloooooooooooooo", City)
    # 1. Connect to DB
    # 2. Check username is used or not
    # 3. Insert to DB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    #  client = boto3.Session(region_name='us-east-1', profile_name='dev').client('dynamodb')
    table = dynamodb.Table('city')
    print("hi", table)
    response = table.scan(FilterExpression=Key('name').eq(City))
    print(response)
    # response = table.get_item(
    # Key={
    # 'userId': userId,
    # 'name': username
    # }
    # )
    # return render_template('base.html')
    return render_template('search.html', form=form)


@webapp.route('/register', methods=['GET', 'POST'])
def register():
    """ Go to the register page.

    After the user submit the register form (username, password and confirmed
    confirmed password included), the browser side invalidate all inputs and 
    check whether username exist in database or not. If not, insert the user 
    information into database ('users' table), and jump to login page; otherwise,
    falsh a warning and ask the user to register again.
    
    """
    form = RegisterForm()
    #userId = request.form.get('userId')
    username = request.form.get('username')
    password = request.form.get('password')

    if form.reset.data:  # if click "Reset"
        return redirect(url_for('register'))

    if form.validate_on_submit():
        # 1. Connect to DB
        # 2. Check username is used or not
        # 3. Insert to DB
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        #  client = boto3.Session(region_name='us-east-1', profile_name='dev').client('dynamodb')
        table = dynamodb.Table('user')

        userId = stringUtils.randomString(10)
        # here salt is created
        salt = stringUtils.randomString(12)
        encPwd = stringUtils.encryptString(password + salt)

        response = table.scan(FilterExpression=Key('name').eq(username))
        # response = table.get_item(
        # Key={
        # 'userId': userId,
        # 'name': username
        # }
        # )
        print(response)

        for i in response["Items"]:
            if username == i["name"]:

                # if username in response["Items"]["name"]:

                flash('User exists! Please try different Username')
                return redirect(url_for('register'))

        else:
            print("HI")
            response = table.put_item(
                Item={
                    'userId': userId,
                    'name': username,
                    'password': encPwd,
                    'salt': salt,
                    'schedules': [],
                    'cart': []
                })
            flash('Registration Success! Please login.', 'success')
            #res=dynamodb.scan(table)
            #print(res)
            return redirect(url_for('login'))

            # return render_template('/uploading.html')
    return render_template('register.html', form=form)


@webapp.route('/login', methods=['GET', 'POST'])
def login():
    """ Go to the login page.
    
    After the client post the user information (username and password), connect 
    to database to check whether the username exists and match with password.
    
    If both username and password are valid, add username to the session and 
    jump to homepage; otherwise, falsh a warning and ask to insert username and 
    password again.

    """
    form = LoginForm()
    username = request.form.get('username')
    print("yoooooooooooooooooooo", username)
    password = request.form.get('password')

    if form.validate_on_submit():
        # 1. Connect to DB
        # 2. Query username
        # 3. Check whether exist and password

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('user')
        #client=boto3.client('dynamodb',region_name='us-east-1')
        #user_result=client.get_item(TableName='user', Key={'userId':{'S':str(userId)},'name':{'S':str(name)}}

        response = table.scan(
            FilterExpression=Key('name').eq(username)
            #ProjectionExpression="userId, name, password,salt",
            # # ExpressionAttributeNames=ean
        )

        # response = table.get_item(
        # Key={
        # 'userId': userId,
        # # 'name': username,
        # #'password':password,
        # #'salt':salt
        # }
        # )
        #print (user_result)

        # response = table.query(
        # KeyConditionExpression=Key('name').eq(username)
        # )
        print(response)
        if "Items" in response and len(response['Items']) > 0:
            items = response['Items']
            #return items[0]

            pwd_db = items[0]["password"]

            salt = items[0]["salt"]

            # pwd_db = items.get("password")
            # salt = items.get("salt")
            encPwd = stringUtils.encryptString(password + salt)
            if pwd_db != encPwd:
                flash('Wrong password!', 'warning')
                return redirect(url_for('login'))
            else:
                session.permanent = True
                session['username'] = items[0]["name"]
                session['userId'] = items[0]["userId"]
                return redirect(url_for('home'))
        else:
            flash('Invalid username! Try again or create a new account.',
                  'warning')
            return redirect(url_for('login'))

    return render_template("login.html", form=form)


@webapp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
