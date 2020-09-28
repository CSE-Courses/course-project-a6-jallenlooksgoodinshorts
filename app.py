from flask import Flask, render_template, url_for, redirect, flash
from forms import LoginForm, RegistrationForm
from db import newUser, loginUser
from flask_login import LoginManager, login_user, current_user, login_required, UserMixin
#from flask_bcrypt import Bcrypt
import bcrypt

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
    if form.validate_on_submit():
        email = form.email
        hashedPassword = bcrypt.hashpw(form.password, bcrypt.gensalt())

        authenticatedUser = loginUser(email, hashedPassword)

        if authenticatedUser != None:

            newUserType = User(authenticatedUser)
            login_user(newUserType)

            flash('Success', 'success')

            return redirect(url_for('welcome'))
        else :
            flash('Incorrect email or password', 'warning')
            return redirect(url_for('login'))

    return render_template('login.html', title = 'Login')

@app.route('/register',  methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        firstName = form.firstname
        lastName = form.lastname
        email = form.email
        hashedPassword = bcrypt.hashpw(form.password, bcrypt.gensalt())
        username = form.username

        # register a new user usign db command newUser and reurn email
        newUserAuth = newUser(email, hashedPassword, firstName, lastName, username)

        if newUserAuth != None:

            flash('Account Created!', 'success')

            return redirect(url_for('login'))
        else : 
            flash('Incorrect email or password', 'warning')

    return render_template('register.html', title = 'Register')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
0