import os

basedir = os.path.abspath(os.path.dirname(__file__))

# except we want emaiil for debuggin in prod
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None
ADMINS = ['you@example.com']
