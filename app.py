from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from forms import LoginForm, RegistrationForm, PostForm, EditForm, ProfileLookupForm, ChangeProfilePicture, CommentForm, securityForm
from flask_login import LoginManager, login_user, current_user, login_required, UserMixin, logout_user
from flask_bcrypt import Bcrypt
import bcrypt
import sys
import db
import os
import csv
import time
import json
import secrets
import gunicorn
import db
from textblob import TextBlob
from base64 import b64encode


# Runs Bcrypt on server

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you_killed_my_father_prepare_to_die'
port = int(os.environ.get("PORT", 5000))

login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, id):
        user = id
        self.id = id

    def get_user(id):
        user = User(id)
        return user


@login_manager.user_loader
def load_user(id):
    return User.get_user(id)


db.testConn()


bcrypt = Bcrypt(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/browse', methods=['GET', 'POST'])
def browse():

    activityList = db.getAllActivities()
    activities = []

    for activ in activityList:
        image = b64encode(activ[2]).decode('"utf-8"')
        likes = db.getLikes(activ[4])  # Changed for likes
        if(current_user.is_anonymous == False):
            likeStatus = db.checkLikeDB(current_user.id, activ[4])
        else:
            likeStatus = False
        a = {
            'title': activ[0],
            'description': activ[1],
            'image': image,
            'activity_id': activ[4],
            'likes': likes,
            'likeStatus': likeStatus

        }
        activities.append(a)

    activities.reverse()

    return render_template('browse.html', activities=activities, title='Welcome')


@app.route('/activityfeed', methods=['GET', 'POST'])
@login_required
def activityfeed():
    activityIDs = db.getActivityIDs(current_user.id)
    activities = []

    print("Activity IDs", file=sys.stderr)
    print(activityIDs, file=sys.stderr)
    if activityIDs:
        if activityIDs[0]:
            for ids in activityIDs:
                activ = db.getActivity(ids[0])
                if(current_user.is_anonymous == False):
                    likeStatus = db.checkLikeDB(current_user.id, activ[4])
                else:
                    likeStatus = False
                print("ACTIV", file=sys.stderr)
                print(activ[0].decode(), file=sys.stderr)
                image = b64encode(activ[2]).decode('"utf-8"')
                likes = db.getLikes(activ[4])  # Changed for likes

                a = {
                    'title': activ[0].decode(),
                    'description': activ[1].decode(),
                    'image': image,
                    'activity_id': activ[4],
                    'likes': likes,
                    'likeStatus': likeStatus
                }

                activities.append(a)

    activities.reverse()

    return render_template('feed.html', activities=activities, title='Activities')


@app.route('/activity/<int:activity_id>', methods=['GET', 'POST'])
def activity(activity_id):
    likeStatus = db.checkLikeDB(current_user.id, activity_id)
    activ = db.getActivity(activity_id)
    members = db.getActivityUsers(activity_id)
    image = b64encode(activ[2]).decode('"utf-8"')
    likes = db.getLikes(activity_id)  # Changed for likes

    happydisplay = None

    if activ[8] != 0:
        num = int(round(((activ[5] * 100) / activ[8]), 2))
        happydisplay = "People are " + str(num) + "% happy with this activity"
    else:
        happydisplay = "Not enough coments to see how happy people are with this activity."

    a = {
        'title': activ[0].decode(),
        'description': activ[1].decode(),
        'image': image,
        'activity_id': activ[4],
        'likes': likes,
        'happy': happydisplay
    }

    # Setting the sentiments for the activity
    happy = activ[5]
    neutral = activ[6]
    sad = activ[7]
    totalComments = activ[8]

    dbcomments = db.getcomments(activity_id)
    comments = []
    if dbcomments:
        if dbcomments[0]:
            for comms in dbcomments:
                fname = db.firstNameUser(comms[1])
                print("USER ID --------------- Comment", file=sys.stderr)
                print(comms, file=sys.stderr)
                print(fname, file=sys.stderr)
                c = {
                    'username': str(db.firstNameUser(comms[1]))[2:-3],
                    'body': comms[2]
                }
                comments.append(c)

    form = CommentForm()

    print("-------- PRE FORM ----------", file=sys.stderr)
    if form.validate_on_submit():
        body = form.comment.data
        print("Activity ID --------------- Comment", file=sys.stderr)
        print(current_user.id, file=sys.stderr)

        # Comment Sentiment Analysis
        text = TextBlob(body)
        sentiment = text.polarity

        if (sentiment > 0.4):
            happy += 1
        elif (sentiment < 0):
            sad += 1
        else:
            neutral += 1

        totalComments += 1

        print(sentiment, file=sys.stderr)

        db.updateSentiments(activity_id, happy, neutral, sad, totalComments)

        # End Analysis
        buff = db.writecomment(current_user.id, activity_id, body)
        return redirect(url_for('activity', activity_id=activity_id))

    return render_template('activity.html', comments=comments, title='Activity', members=members, form=form, activity=a, likeStatus=likeStatus, likes=likes)


@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.body.data
        image = form.image.data.read()
        activity_id = db.createActivity(title, description, image, 0)
        print("Activity ID", file=sys.stderr)
        print(activity_id, file=sys.stderr)
        db.joinActivityDB(current_user.id, activity_id)

        return redirect(url_for('browse'))

    return render_template('newPost.html', title='Post', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        unhashedPassword = form.password.data
        hashedPassword = getPassword(email)

        print("PASSWORDS", file=sys.stderr)
        print(unhashedPassword, file=sys.stderr)
        print(hashedPassword, file=sys.stderr)

        if bcrypt.check_password_hash(hashedPassword[0].decode(), unhashedPassword):
            signedIn = User(email)
            login_user(signedIn)
            return redirect(url_for('browse'))
        else:
            flash(
                'Incorrect login information. Try again or register for an account', 'error')
            return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)


@app.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        firstName = form.firstname.data
        lastName = form.lastname.data
        email = form.email.data
        password = form.password.data
        username = form.username.data

        hashedPassword = bcrypt.generate_password_hash(
            password).decode('utf-8')

        db.newUser(email, hashedPassword, firstName, lastName, username)

        with open('userpass.txt', mode='w') as csvfile:
            writeme = csv.writer(csvfile)
            writeme.writerow([email, hashedPassword])
            csvfile.close()

        flash('account created', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/joinactivity/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def joinactivity(activity_id):  # joinactivity = server, joinActivity = sql
    db.joinActivityDB(current_user.id, activity_id)
    return redirect(url_for('activityfeed'))


@app.route('/profileinquiry', methods=['GET', 'POST'])
@login_required
def searchprofile():
    form = ProfileLookupForm()
    substringedForm = []
    returnedInfo = []
    addedUser = []

    print("Search Input --------------------------", file=sys.stderr)
    print(form.accproperty.data, file=sys.stderr)

    if form.validate_on_submit():
        for length in range(1, len(form.accproperty.data)+1):
            substringedForm.append(form.accproperty.data[0:length])

        substringedForm.reverse()

        for substr in substringedForm:
            infoRet = db.userInfoInquiry(substr)
            for infoUser in infoRet:
                if infoUser[0] not in addedUser:
                    addedUser.append(infoUser[0])
                    returnedInfo.append(infoUser)

        print("Returned Info Result ------------", file=sys.stderr)
        print(returnedInfo, file=sys.stderr)

        return render_template('profileinquiry.html', title='search', form=form, returnedInfo=returnedInfo)

    return render_template('profileinquiry.html', title='search', form=form)


@ app.route('/otherprofile/<string:user_id>', methods=['GET', 'POST'])
@ login_required
def vprofile(user_id):
    activityIDs = db.getActivityIDs(user_id)
    returnedInfo = db.userInfo(user_id)
    print("RETURNEDINFO", flush=True)
    print(returnedInfo, flush=True)
    activities = []
    print("User ID", file=sys.stderr)
    print(user_id, file=sys.stderr)

    print("Activity IDs", file=sys.stderr)
    print(activityIDs, file=sys.stderr)
    if activityIDs:
        if activityIDs[0]:
            for ids in activityIDs:
                activ = db.getActivity(ids[0])

                print("ACTIV", file=sys.stderr)
                print(activ, file=sys.stderr)
                image = b64encode(activ[2]).decode('"utf-8"')
                likes = 0  # Change for likes

                a = {
                    'title': activ[0].decode('"utf-8"'),
                    'description': activ[1].decode('"utf-8"'),
                    'image': image,
                    'activity_id': activ[4]
                }
                activities.append(a)

    activities.reverse()

    return render_template('otherprofile.html', activities=activities, title='Activities', returnedInfo=returnedInfo)


@ app.route('/profile')
@ login_required
def profile():
    activityIDs = db.getActivityIDs(current_user.id)
    activities = []
    if activityIDs:
        if activityIDs[0]:
            for ids in activityIDs:
                activ = db.getActivity(ids[0])
                image = b64encode(activ[2]).decode('"utf-8"')
                likes = 0  # Change for likes

                a = {
                    'title': activ[0].decode(),
                    'description': activ[1].decode(),
                    'image': image,
                    'activity_id': activ[4]
                }
                activities.append(a)

    activities.reverse

    i = db.getInfo(current_user.id)

    info = {
        'about': i[0].decode(),
        'interests': i[1].decode(),
        'location': i[2],
        'gender': i[3].decode(),
        'email': i[4].decode()}
    picDb = db.getPic(current_user.id)

    if(picDb != None):
        pic = b64encode(picDb[0]).decode('"utf-8"')

    else:
        pic = None
    return render_template('profile.html', activities=activities, title='Activities', info=info, pic=pic)


@ app.route('/profileSettings')
@ login_required
def profileSettings():
    print("Current User ID", file=sys.stderr)
    print(current_user.id, file=sys.stderr)

    i = db.getInfo(current_user.id)

    info = {'about': i[0].decode(), 'interests': i[0].decode(
    ), 'location': i[0], 'gender': i[0], 'email': i[0]}
    picDb = db.getPic(current_user.id)
    print(picDb, file=sys.stderr)
    if(picDb != None):
        pic = b64encode(picDb[0]).decode('"utf-8"')

    else:
        pic = None
    return render_template('db.settings.html', info=info, pic=pic)


@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def editInfo():
    form = EditForm()

    if form.validate_on_submit():
        print(current_user.id, file=sys.stderr)
        about = form.about.data
        interests = form.interests.data
        location = form.location.data
        gender = form.gender.data
        i = db.getInfo(current_user.id)
        if(about == ""):
            about = i[0][0]
        if(interests == ""):
            interests = i[0][1]
        if(location == ""):
            location = i[0][2]
        if(gender == ""):
            gender = i[0][3]
        print(about, file=sys.stderr)
        print(interests, file=sys.stderr)

        db.editInfo(current_user.id, about, interests, location, gender)
        print(form.errors, file=sys.stderr)
        return redirect(url_for('profile'))
    print(form.errors, file=sys.stderr)
    return render_template('editProfile.html', title='Edit', form=form)


@app.route('/securitySettings', methods=['GET', 'POST'])
@login_required
def editSettings():
    form = securityForm()

    if form.validate_on_submit():
        print(current_user.id, file=sys.stderr)
        username = form.username.data
        password = form.password.data
        i = db.getInfo(current_user.id)
        if(username == ""):
            username = i[0][5]
        if(password == ""):
            password = i[0][6]
        db.settings(username, password, current_user.id)
        print(form.errors, file=sys.stderr)
        return redirect(url_for('profile'))
    print(form.errors, file=sys.stderr)
    return render_template('securitySettings.html', title='Edit', form=form)


@app.route('/changePicture', methods=['GET', 'POST'])
@login_required
def editProfPic():
    form = ChangeProfilePicture()
    if form.validate_on_submit():
        picture = form.picture.data.read()
        i = db.changeProfPic(current_user.id, picture)
        print(i, file=sys.stderr)
        return redirect(url_for('profile'))

    return render_template('changePicture.html', title='Profile Picture', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/likepost/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def likepost(activity_id):
    activ = db.getActivity(activity_id)
    title = activ[0]
    db.addLike(title, current_user.id, activity_id)
    return('', 204)


@app.route('/unlikepost/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def unlikepost(activity_id):
    activ = db.getActivity(activity_id)
    print(activ[4], file=sys.stderr)
    db.removeLike(current_user.id, activ[4])
    return('', 204)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)

# Testing dev branch merge
