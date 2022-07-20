from flask import Flask, render_template
from flask_moment import Moment
from datetime import datetime

from forms import RegistrationForm, LoginForm

app = Flask(__name__)
moment = Moment(app)

app.config['SECRET_KEY'] = 'test_secret'


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('authpage.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('authpage.html', form=form)


if __name__ == __name__:
    app.run(debug=True)
