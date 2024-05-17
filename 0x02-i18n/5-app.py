#!/usr/bin/env python3
""" 3. Parametrize templates
"""

from flask_babel import Babel
from flask import Flask, render_template, request, g

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Config class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ get_locale function
    """
    requested_locale = request.args.get('locale')
    if requested_locale and requested_locale in app.config['LANGUAGES']:
        return requested_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """ get_user function
    """
    user_login = request.args.get('login_as')
    if user_login is not None and user_login.isdigit() and int(user_login) in users:
        return users[int(user_login)]
    return None



@app.before_request
def before_request():
    """ before_request function
    """
    g.user = get_user()
    print(g.user)


@app.route('/')
def index():
    """ Index route
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(debug=True)
