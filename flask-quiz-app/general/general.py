from flask import Blueprint, redirect, render_template

general_bp = Blueprint('general', __name__, 
    template_folder='templates', static_folder='static', static_url_path='flask-quiz/app/general/static')

@general_bp.route('/')
def home():
    return render_template('home.html')
