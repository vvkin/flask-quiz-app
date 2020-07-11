from flask import Blueprint, redirect, render_template

general_bp = Blueprint('general', __name__, 
    template_folder='templates', static_folder='static')

@general_bp.route('/home')
def home():
    return render_template('home.html')
