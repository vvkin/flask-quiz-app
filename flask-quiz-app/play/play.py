from flask import Blueprint, g, render_template, request, redirect, flash, url_for, \
    session, abort
from ..db import get_db
from ..auth.auth import login_required
import requests
import functools

play_bp = Blueprint('play', __name__, static_folder='static', template_folder='templates')

def started_game_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'q_number' in session and request.method != 'POST':
            return redirect(url_for('play.play'))
        return view(**kwargs)
    return wrapped_view

@play_bp.route('/', methods=('GET', 'POST'))
@login_required
def play():
    if request.method == 'POST':
        q_number = int(request.form['diff_button'])
        get_questions_set(q_number)
        return redirect(url_for('play.display_question'))
    return render_template('play.html')

@play_bp.route('/question/', methods=('GET', 'POST'))
@started_game_required
@login_required
def display_question():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == session['q_set'][session['q_number']]['correct']:
           session['c_number'] += 1
        session['q_number'] += 1
        return redirect(url_for('play.display_question'))

    if session['q_number'] == len(session['q_set']):
        return redirect(url_for('play.display_results'))
    
    current_question = session['q_set'][session['q_number']]
    return render_template('question.html', question=current_question, 
        q_number=session['q_number'])

def get_questions_set(q_number):
    url = f'https://opentdb.com/api.php?amount={q_number}'
    response = requests.get(url)
    q_json = response.json()
    data = []
   
    for q_info in q_json['results']:
        all_answers = [q_info['correct_answer']] + q_info['incorrect_answers']
        data.append({'correct' : q_info['correct_answer'], 
        'all_answers' : all_answers, 'text': q_info['question']})

    session['q_set'] = data
    session['c_number'] = 0
    session['q_number'] = 0

def update_rating(q_number, c_number):
    db = get_db()
    old_values = db.execute('SELECT * FROM Rating WHERE id = ?', 
    (g.user['rating'], )).fetchone()
    rating = dict(old_values)
    rating['answers_number'] += q_number
    rating['correct_answers'] += c_number
    rating['wrong_answers'] += q_number - c_number
    rating['correct_percent'] = round(rating['correct_answers']/rating['answers_number'], 2)
    db.execute('''UPDATE Rating SET
        answers_number = ?,
        correct_answers = ?,
        wrong_answers = ?,
        correct_percent = ?
        WHERE id=?''', tuple(rating.values())[1:5] + (g.user['rating'],))
    db.commit()

@play_bp.route('/results/', methods=('GET', 'POST'))
@started_game_required
@login_required
def display_results():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == 'tohome':
            return redirect(url_for('general.home'))
        else:
            return redirect(url_for('play.play'))

    q_number = session.pop('q_number')
    c_number = session.pop('c_number')
    update_rating(c_number, q_number)
    return render_template('results.html',c_number=c_number, q_number=q_number)

