from flask import Flask
from datetime import timedelta

from config import SECRET_KEY
from flask import Blueprint
webapp = Flask(__name__)
webapp.config["SECRET_KEY"] = SECRET_KEY
#webapp.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
#webapp.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

from app import login
#from app.api import blueprint as api

api = Blueprint('api', __name__)
webapp.register_blueprint(api, url_prefix='/api')
