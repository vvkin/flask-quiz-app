from flask import Blueprint, request, session, render_template, flash, redirect, url_for, g
from werkzeug.security import check_password_hash, generate_password_hash
from ..db import get_db
import functools

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@auth_bp.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        error = None
        db = get_db()
        full_name = request.form['u_name']
        email = request.form['u_email']
        username = request.form['username']
        password = request.form['u_passwd']

        if db.execute('SELECT id FROM user WHERE username=?', 
        (username, )).fetchone() is not None:
            error = 'Username is already exist!'
        elif db.execute('SELECT id FROM user WHERE email=?',
        (email, )).fetchone() is not None:
            error = 'Email is used by another user!'
        else:
            db.execute('''INSERT INTO Rating 
            (answers_number, correct_answers, wrong_answers, correct_percent)
            VALUES(?,?,?,?)''', (0, 0, 0, 0))
            rating_id = db.execute('SELECT id FROM Rating ORDER BY id DESC').fetchone()[0]
            db.execute('''INSERT INTO User (full_name, username, email, password, rating) 
            VALUES (?, ?, ?, ?, ?)''', 
                (full_name, username, email, 
                generate_password_hash(password), rating_id))
            db.commit()
            flash('You have been succesfully signed up', category='success')
            return redirect(url_for('general.home'))

        flash(error)

    return render_template('register.html')

@auth_bp.route('/login/', methods=('GET', 'POST'))
def login():
    if g.user:
            flash('You already logged in')
            return redirect(url_for('general.home'))
    if request.method == 'POST':
        error = None
        db = get_db()
        username = request.form['username']
        password = request.form['password']
        user = db.execute('SELECT * FROM User WHERE username=?', (username, )).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash('You have been successfully logged in', category='success')
            return redirect(url_for('general.home'))
        flash(error)
    return render_template('login.html')

@auth_bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('general.home'))

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM User WHERE id=?', (user_id, )
        ).fetchone()