from flask import Blueprint, redirect, render_template, url_for, request, g

general_bp = Blueprint('general', __name__, 
    template_folder='templates', static_folder='static', static_url_path='flask-quiz/app/general/static')

@general_bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        if g.user:
            return redirect(url_for('play.play'))
        else:
            return redirect(url_for('auth.register'))
    return render_template('home.html')
