from flask import Flask
from datetime import timedelta

from config import SECRET_KEY
from app.utils import urlUtils
webapp = Flask(__name__)
webapp.config["SECRET_KEY"] = SECRET_KEY
#webapp.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
#webapp.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!############
############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!############
############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!############
############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!############
############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!############
####### COMMENT THIS LINE WHEN DEPLOY ON LAMBDA #######
####### COMMENT THIS LINE WHEN DEPLOY ON LAMBDA #######
####### COMMENT THIS LINE WHEN DEPLOY ON LAMBDA #######
####### COMMENT THIS LINE WHEN DEPLOY ON LAMBDA #######
webapp.wsgi_app = urlUtils.PrefixMiddleware(webapp.wsgi_app, prefix='/dev')

from app import city
from app import schedule
from app import user
from app import login
from app import search