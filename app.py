from flask import Flask, render_template
from flask_moment import Moment
from datetime import datetime

from forms import NameFormTest

app = Flask(__name__)
moment = Moment(app)

app.config['SECRET_KEY'] = 'implement-os-module-here'


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = NameFormTest()
    return render_template('authpage.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = NameFormTest()
    form.user_email.label = 'Email:'
    form.password.label = 'Password:'
    return render_template('authpage.html', form=form)


if __name__ == __name__:
    app.run(debug=True)
