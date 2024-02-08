import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)

usr = Blueprint('user', __name__, url_prefix='/user', static_folder='static', static_url_path='blueprints/user/static')



