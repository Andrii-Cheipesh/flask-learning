import os
from archi import create_app

app = create_app(os.getenv('FLASK_CONFIG', 'default'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

    # testing commit in PR