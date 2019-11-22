from flask import render_template, session, flash, redirect, url_for
from flask_bootstrap import Bootstrap
import boto3
from boto3.dynamodb.conditions import Key, Attr

from app.utils.utils import *
from app.forms import RegisterForm, LoginForm
from app import webapp

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
bootstrap = Bootstrap(webapp)


@webapp.route('/user_page/<uid>')
def user_page(uid):
    table = dynamodb.Table('user')

    # userId = '100010'
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

@webapp.route('/view_schedule/<scheduleName>')
def view_schedule(scheduleName):
    return scheduleName


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
        cnx = get_db()
        cursor = cnx.cursor()

        # here salt is created
        salt = randomString(12)
        encPwd = encryptString(password + salt)

        query = '''SELECT * FROM users WHERE userID = %s'''
        cursor.execute(query, (username,))
        if cursor.fetchone() is not None:
            flash('The username is used.', 'warning')
            return redirect(url_for('register'))  # not sure
        else:
            query = '''INSERT INTO users (userID, password, salt) VALUES (%s, %s, %s)'''
            cursor.execute(query, (username, encPwd, salt))
            cnx.commit()
            flash('Registration Success! Please login.', 'success')
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
    password = request.form.get('password')

    if form.validate_on_submit():
        # 1. Connect to DB
        # 2. Query username
        # 3. Check whether exist and password
        cnx = get_db()
        cursor = cnx.cursor()

        query = '''SELECT * FROM users WHERE userID = %s'''
        cursor.execute(query, (username,))
        user_result = cursor.fetchone()
        if user_result is None:
            flash('Invalid username! Try again or create a new account.', 'warning')
            return redirect(url_for('login'))
        else:
            pwd_db = user_result[1]
            salt = user_result[2]
            encPwd = encryptString(password + salt)
            if pwd_db != encPwd:
                flash('Wrong password!', 'warning')
                return redirect(url_for('login'))
            else:
                flash('Login Success!', 'success')
                session.permanent = True
                session['username'] = username
                return redirect(url_for('index'))
    return render_template("login.html", form=form)


@webapp.route('/logout')
def logout():
    session.clear()
    flash('You were logged out', 'success')
    return redirect(url_for('index'))
