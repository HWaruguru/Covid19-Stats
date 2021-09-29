from flask import Blueprint
from flask_cors import CORS


main = Blueprint('main',__name__)
CORS(main, resources='*')

from . import views