from __future__ import print_function # Python 2/3 compatibility
from flask import render_template, request, url_for, redirect, flash, session
from flask_bootstrap import Bootstrap

from app.forms import RegisterForm, LoginForm
from app.utils import *
from app import webapp
bootstrap = Bootstrap(webapp)


import boto3
from botocore.exceptions import ClientError
import json
from boto3.dynamodb.conditions import Key, Attr


@webapp.route('/',methods=['GET', 'POST'])
@webapp.route('/index',methods=['GET', 'POST'])
def index():
    
    
    City = request.form.get('inputcity')
    if City:
        
        # 1. Connect to DB
        # 2. Check username is used or not
        # 3. Insert to DB
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

        table = dynamodb.Table('city')

        response = table.scan(
        FilterExpression=Key('name').eq(City)
            )
        if response["Items"]:
            for i in response["Items"]:
                if City == i["name"]:
                    cityId=i["cityId"]
                    session['cityname'] = City
        
                return redirect(url_for('search',cityId=cityId,city=City)) 
        else:
            flash('City does not exist. Please try another','warning')
    
    
    is_login = False
    username = ""
    if session.get('username') is not None:
        is_login = True
        username = session.get('username')
    return render_template('base.html', is_login=is_login, username=username) 

@webapp.route('/search/<cityId>/<city>',methods=['GET','POST'])   
def search(cityId,city):

    if session.get('cityname') is not None:
        city = session.get('cityname')
        
    is_login = False
    username = ""
    if session.get('username') is not None:
        is_login = True
    
    return render_template('search.html',city=city,is_login=is_login) 
    

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

    username = request.form.get('username')
    password = request.form.get('password')

    if form.reset.data:  # if click "Reset"
        return redirect(url_for('register'))

    if form.validate_on_submit():
        # 1. Connect to DB
        # 2. Check username is used or not
        # 3. Insert to DB
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
   
        table = dynamodb.Table('user')
        
        userId=randomString(10)
        # here salt is created
        salt = randomString(12)
        encPwd = encryptString(password + salt)
        
        response = table.scan(
        FilterExpression=Key('name').eq(username)
        )

        print(response)
        
        for i in response["Items"]:
            if username == i["name"]:
                     
                print("User exists")
                flash('User exists! Please try different Username','warning')
                return redirect(url_for('register'))

        else:

            response = table.put_item(
            Item={
           'userId': userId,
           'name': username,
           'password':encPwd,
           'salt':salt}
         )
            flash('Registration Success! Please login.', 'success')

            return redirect(url_for('login'))
   
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

    password = request.form.get('password')

    if form.validate_on_submit():
        # 1. Connect to DB
        # 2. Query username
        # 3. Check whether exist and password


        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('user')

       
        response = table.scan(
        FilterExpression=Key('name').eq(username)
         )       
 
        if "Items" in response:
            items=response['Items']
            
            pwd_db=items[0]["password"]
            
            salt=items[0]["salt"]

            encPwd = encryptString(password + salt)
            if pwd_db != encPwd:
                flash('Wrong password!', 'warning')
                return redirect(url_for('login'))
            else:
                flash('Login Success!', 'success')
                session.permanent = True
                session['username'] = items[0]["name"]
                return redirect(url_for('index'))
        else:
            flash('Invalid username! Try again or create a new account.', 'warning')
            return redirect(url_for('login'))


    return render_template("login.html", form=form)


@webapp.route('/logout')
def logout():
    session.clear()
    flash('You were logged out', 'success')
    return redirect(url_for('index'))
