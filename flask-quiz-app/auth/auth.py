from flask import Blueprint, request, session, render_template, flash

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth', template_folder='templates/auth')

@auth_bp.route('/register')
def register():
    if request.method == 'POST':
        error = None
        first_name = request.form['uf_name']
        second_name = request.form['us_name']
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
        
        if error is not None:
            flash(error)
            return render_template('register.html')

        # DB connection is needed

    return render_template('register.html')