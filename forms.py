from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired


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
    accproperty = StringField('Enter the Account Name', validators=[(DataRequired())])
    submit = SubmitField("Look Up")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg'])])
    submit = SubmitField('Create Activity')

<<<<<<< HEAD
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Submit')
=======
class EditForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    about = StringField('About')
    interests = StringField('Interests')
    submit = SubmitField('Edit Info')

>>>>>>> 73e5ab5db90db5e90c6b4c495d2ed2a00ef309ac
