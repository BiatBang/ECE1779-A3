from flask import Flask

webapp = Flask(__name__)

from app import city
from app import schedule
from app import user