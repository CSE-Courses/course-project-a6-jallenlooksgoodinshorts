from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html', title = 'Login')

@app.route('/register',  methods = ['GET', 'POST'])
def register():
    return render_template('register.html', title = 'Register')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
