from flask import Flask, render_template
from forms import LoginForm, RegistrationForm
from db import newUser, loginUser
from flask_login import LoginManager, login_user, current_user
#from flask_bcrypt import Bcrypt
import bcrypt

#Runs Bcrypt on server 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you_killed_my_father_prepare_to_die'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/welcome')
def welcome():
    return render_template('Welcome.html', title = 'Welcome')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email
        hashedPassword = bcrypt.hashpw(form.password, bcrypt.gensalt())

        authenticatedUser = loginUser(email, hashedPassword)
        login_user(authenticatedUser)


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
        newUser(email, hashedPassword, firstName, lastName, username)
        flash('Account Created!')

        return app.redirect(url_for('login'))

    return render_template('register.html', title = 'Register')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
0