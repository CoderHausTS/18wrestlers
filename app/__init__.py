from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from .logging_config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from .momentjs import momentjs

mail = Mail()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.jinja_env.globals['momentjs'] = momentjs

mail.init_app(app)

# let's init down below instead
db = SQLAlchemy(app)

#get our views and stuff
from app import views

#  needed to move this import way down because of a circular ref.  Who knew?
if app.config["API_V1_TOGGLE"]:
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')


# turn on debug logging to email and file if debug mode FALSE
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler

    #mail logging
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # file logging
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')
