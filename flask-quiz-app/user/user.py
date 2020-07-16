from flask import Blueprint, url_for, render_template, redirect, g
from ..db import get_db

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')


def get_user_data(username):
    db = get_db()
    user = g.user
    if user is None or g.user['username'] != username:
        user = db.execute('SELECT * FROM User WHERE username=?',
            (username,)).fetchone()
    rating = db.execute('SELECT * FROM Rating WHERE id=?', 
        (user['rating'],)).fetchone()
    return user, rating

@user_bp.route('/<username>/')
def user_page(username):
    user, rating = get_user_data(username)
    return render_template('user_page.html', user=user, rating=rating)


