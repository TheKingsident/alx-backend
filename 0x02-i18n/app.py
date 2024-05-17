#!/usr/bin/env python3
""" 3. Parametrize templates
"""

import pytz
from flask_babel import Babel
from datetime import datetime
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
    # Locale from URL parameters
    requested_locale = request.args.get('locale')
    if requested_locale and requested_locale in app.config['LANGUAGES']:
        return requested_locale

    # Locale from user settings
    if g.user and 'locale' in g.user and g.user['locale'] in app.config[
            'LANGUAGES']:
        return g.user['locale']

    # Locale from request header
    apt_lang = request.accept_languages.best_match(app.config['LANGUAGES'])
    if apt_lang:
        return apt_lang

    # Default locale
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """ get_timezone function
    """
    # Timezone from URL parameters
    requested_timezone = request.args.get('timezone')
    if requested_timezone:
        try:
            pytz.timezone(requested_timezone)
            return requested_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Timezone from user settings
    if g.user and 'timezone' in g.user:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Default to UTC
    return 'UTC'


def get_user():
    """ get_user function
    """
    user_login = request.args.get('login_as')
    if user_login is not None and int(user_login) in users:
        return users.get(int(user_login))
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
    current_time = datetime.now(pytz.timezone(get_timezone()))
    return render_template('index.html',
                           current_time=current_time.strftime(
                               '%b %d, %Y, %I:%M:%S %p'))


if __name__ == '__main__':
    app.run(debug=True)
