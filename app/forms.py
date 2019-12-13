from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            Length(min=4, max=20)
        ])
    password = PasswordField(
        'Password',
        validators=[
            Length(min=6, max=30),
            EqualTo('confirm', message='Password must match.')
        ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')
    reset = SubmitField('Reset')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('search', validators=[InputRequired()])