from flask import Flask
from app.utils import urlUtils

webapp = Flask(__name__)

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
from app import search