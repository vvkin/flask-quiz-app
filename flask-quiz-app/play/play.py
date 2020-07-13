from flask import Blueprint, render_template
import os

play_bp = Blueprint('play', __name__, static_folder='static', template_folder='templates')

@play_bp.route('/')
def play():
    return render_template('play.html')



