from flask import Flask, render_template, url_for, redirect, flash
from forms import LoginForm, RegistrationForm
import db
from flask_login import LoginManager, login_user, current_user, login_required, UserMixin
from flask_bcrypt import Bcrypt
import bcrypt
import sys
import os
import csv
import secrets
from csv import reader

#Runs Bcrypt on server 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you_killed_my_father_prepare_to_die'

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return User.get_user(id)

class User(UserMixin):
    def __init__(self, id):
        user = id
        self.id = id

    def get_user(id):
        user = User(id)
        return user

db.testConn()


bcrypt = Bcrypt(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', title = 'Welcome')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() :
        email = form.email.data
        hashedPassword = form.password.data

        valid = False

        with open('userpass.txt', mode='r') as csvfile:
            readme = reader(csvfile)
            for row in reader:
                if row[0] == email:
                    if row[1] == hashedPassword:
                        valid = True

        

        return redirect(url_for('welcome'))

    return render_template('login.html', title = 'Login', form=form)

@app.route('/register',  methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    # if form.validate_on_submit():

    # firstName = form.firstname.data
    # lastName = form.lastname.data
    # email = form.email.data
    # hashedPassword = form.password.data
    # username = form.username.data

    # #     print (firstName)

    # with open('userpass.txt', mode='w') as csvfile:
    #     csv_file = csv.writer(csvfile, delimiter=',')
    #     csv_file.writerow(['test', 'test'])
    #     csv_file.writerow([email, hashedPassword])
    #     csvfile.close()

    if form.validate_on_submit() :
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
0