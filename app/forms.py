from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    # userId = StringField('UserId', validators=[
        # # InputRequired(),
        # Length(min=4, max=20)
    # ])
    username = StringField('Username', validators=[
        # InputRequired(),
        Length(min=4, max=20)
    ])
    password = PasswordField('Password', validators=[
        # InputRequired(),
        Length(min=6, max=30),
        EqualTo('confirm', message='Password must match.')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')
    reset = SubmitField('Reset')

    # reset button


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
         InputRequired()
       
    ])
    # userId = StringField('UserId', validators=[
        # InputRequired()

    # ])
    print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiii",username)
    password = PasswordField('Password', validators=[
        InputRequired()
    ])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('search', validators=[
         InputRequired()
       
    ])


# class UploadForm(FlaskForm):
#     photo = FileField(validators=[
#         FileRequired(message='Please select a photo.'),
#         # FileAllowed(['jpg', 'png'], 'Images only!')
#     ])
#     submit = SubmitField('Upload')
