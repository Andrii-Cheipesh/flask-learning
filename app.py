from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello world!</h1>'


@app.route('/user/<name>')
def user(name):
    return f'<h1>Hi, {name}!</h1>'


if __name__ == __name__:
    app.run(debug=True)
