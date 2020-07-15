from flask import Blueprint, url_for, render_template, redirect, g
from ..db import get_db

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')

@user_bp.route('/<username>/')
def user_page(username):
    user = g.user
    if user is None or username != g.user['username']:
        user = get_db().execute('SELECT * FROM User WHERE username=?',
        (username,)).fetchone()
    return render_template('user_page.html', user=user)

