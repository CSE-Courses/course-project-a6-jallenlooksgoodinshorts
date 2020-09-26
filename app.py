from flask import Flask, render_template
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you_killed_my_father_prepare_to_die'

@app.route('/')
@app.route('/home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Login')

@app.route('/register',  methods = ['GET', 'POST'])
def register():
    form = RegistrationForm
    return render_template('register.html', title = 'Register')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
0