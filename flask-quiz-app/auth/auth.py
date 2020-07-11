from flask import Blueprint, request, session, render_template, flash, redirect, url_for, g
from werkzeug.security import check_password_hash, generate_password_hash
from ..db import get_db

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        error = None
        db = get_db()
        first_name = request.form['uf_name']
        second_name = request.form['us_name']
        username = request.form['username']
        email = request.form['u_email']
        password = request.form['u_pswd']

        if first_name is None:
            error = 'First name is required!'
        elif second_name is None:
            error = 'Second name if required!'
        elif email is None:
            error = 'Email is required!'
        elif password is None:
            error = 'Password is required!'
        elif db.execute('SELECT id FROM user WHERE username=?', 
        (username, )).fetchone() is not None:
            error = 'Username is already exist!'
        elif db.execute('SELCT id FROM user WHERE email=?',
        (email, )).fetchone() is not None:
            error = 'Email is used by another user!'
        
        if error is not None:
            flash(error)
            return render_template('login.html')

        db.execute('INSERT INTO Rating VALUES (?, ?, ?, ?, ?)', 
        ('DEFAULT','DEFAULT', 'DEFAULT', 'DEFAULT', 'DEFAULT'))
        rating_id = db.execute('SELECT id FROM Rating ORDER BY id DESC').fetchone()
        db.execute('INSERT INTO user VALUES (?, ?, ?, ?, ?)', 
            (first_name, second_name, email, username, 
            generage_pasword_hash(password), rating_id))
        db.commit()

        return redirect(url_for('general.index'))

    return render_template('register.html')

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error = None
        db = get_db()
        username = request.form['username']
        password = request.form['passwd']
        user = db.execute('SELECT * FROM User WHERE username=?', (username, ))

        if username is None:
            error = 'Username is required'
        elif password is None:
            error = 'Password is required'
        elif user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('general.home'))
        flash(error)
    return render_template('login.html')

@auth_bp.route('/logout')
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