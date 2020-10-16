from flask import Flask, render_template, url_for, redirect, flash
from db import getActivity, getAllActivities, loginUser, newUser, testConn
from forms import LoginForm, RegistrationForm, PostForm
from flask_login import LoginManager, login_user, current_user, login_required, UserMixin, logout_user
from flask_bcrypt import Bcrypt
import bcrypt
import sys
import db
import os
import csv
import secrets
import gunicorn
from base64 import b64encode

#Runs Bcrypt on server 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you_killed_my_father_prepare_to_die'
port = int(os.environ.get("PORT", 5000))

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

testConn()


bcrypt = Bcrypt(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/activityfeed', methods = ['GET', 'POST'])
@login_required
def activityfeed():

    activityList = getAllActivities()
    activities = []

    for activ in activityList :
        image = b64encode(activ[2]).decode('"utf-8"')
        likes = 0 # Change for likes

        a = {
            'title': activ[0],
            'description': activ[1],
            'image': image,
            'activity_id': activ[4]
            }
        activities.append(a)
        
    activities.reverse

    return render_template('activityfeed.html', activities = activities, title = 'Welcome')

@app.route('/activity/<int:activity_id>', methods = ['GET', 'POST'])
def activity(activity_id):
    activ = getActivity(activity_id)
    image = b64encode(activ[2]).decode('"utf-8"')
    likes = 0 # Change for likes
    a = {
        'title': activ[0],
        'description': activ[1],
        'image': image,
        'activity_id': activ[4]
        }
    return render_template('activity.html', activity = a, title = 'Activity')

@app.route('/newpost', methods = ['GET', 'POST'])
@login_required
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data 
        description = form.body.data
        image = form.image.data.read()
        db.createActivity(title, description, image)

        return redirect(url_for('activityfeed'))

    return render_template('newPost.html', title = 'Post', form=form)
    

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() :
        email = form.email.data
        hashedPassword = form.password.data

        if loginUser(email, hashedPassword) :
            signedIn = User(email)
            login_user(signedIn)
            return redirect(url_for('activityfeed'))
        else :
            return redirect(url_for('register'))

    return render_template('login.html', title = 'Login', form=form)

@app.route('/register',  methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        firstName = form.firstname.data
        lastName = form.lastname.data
        email = form.email.data
        hashedPassword = form.password.data
        username = form.username.data

        newUser(email, hashedPassword, firstName, lastName, username)

        with open('userpass.txt', mode='w') as csvfile:
            writeme = csv.writer(csvfile)
            writeme.writerow([email, hashedPassword])
            csvfile.close()
        
        flash('account created', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Register')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)