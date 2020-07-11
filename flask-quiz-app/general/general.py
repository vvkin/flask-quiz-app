from flask import Blueprint, redirect, render_template

general_bp = Blueprint('general', __name__, template_folder='templates/')

@general_bp.route('/home')
def home_page():
    return render_template('base.html')
