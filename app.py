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
    user_email = None
    form = NameFormTest()
    if form.validate_on_submit():
        user_email = form.user_email.data
        form.user_email.data = ''
    return render_template('register.html', form=form, user_email=user_email)


if __name__ == __name__:
    app.run(debug=True)
