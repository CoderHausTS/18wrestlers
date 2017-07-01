import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WTF_CSRF_ENABLED = True

SITE_NAME = '18Wrestlers.com'
SITE_TAG_LINE = 'Where blogging is a way of life'
SITE_HEAD_IMAGE = '18wrestlers_lg.png'
# pagination
POSTS_PER_PAGE = 5

# turn off email

SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False

# except we want emaiil for debuggin in prod
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None
ADMINS = ['jason@18wrestlers.com']

