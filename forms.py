from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('firstform', validators=[DataRequired(), Email()])
    password = PasswordField('lastform', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    firstname = StringField('firstform', validators=[DataRequired()])
    lastname = StringField('lastform', validators=[DataRequired()])
    email = StringField('emailform', validators=[DataRequired(), Email()])
    password = StringField('passform', validators=[DataRequired()])
    submit = SubmitField('Register')

