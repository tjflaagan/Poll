#configuration file for votr
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'poll.db')
SECRET_KEY = 'development key' # keep this key secret during production
SQLALCHEMY_DATABASE_URI = 'mysql://root:Password1!@127.0.0.1/poll'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True