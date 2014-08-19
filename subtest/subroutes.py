__author__ = 'A'
from flask import Blueprint

subapp = Blueprint('subapp', __name__, url_prefix='/subapp')

@subapp.route('/subpage')
def subpage():
    return 'Subtest success'
