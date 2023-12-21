
from flask import Blueprint

mypay = Blueprint('mypay', __name__)

from . import views