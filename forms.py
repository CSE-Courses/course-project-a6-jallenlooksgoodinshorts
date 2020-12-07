from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, Regexp


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class ProfileLookupForm(FlaskForm):
    accproperty = StringField('Enter the Account Name', validators=[DataRequired(), Regexp('^\w+$')])
    submit = SubmitField("Look Up")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg','.jpg','.jpeg'])])
    submit = SubmitField('Create Activity')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Comment')
    
class EditForm(FlaskForm):
    location = StringField('Location')
    gender = StringField('Gender')
    about = StringField('About', validators=[DataRequired()])
    interests = StringField('Interests', validators=[DataRequired()])
    submit = SubmitField('Edit Info')

class ChangeProfilePicture(FlaskForm):
    picture = FileField('Profile Picture', validators=[DataRequired(), FileAllowed(['jpg','jpeg'])])
    submit = SubmitField('Change Profile Picture')

class securityForm(FlaskForm):
    username = StringField('Change Username')
    password = StringField('Change Password')
    submit = SubmitField('Update username and password')

