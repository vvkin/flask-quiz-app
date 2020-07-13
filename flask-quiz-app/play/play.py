from flask import Blueprint, g, render_template, request, redirect, flash, url_for, session
import json
import requests

play_bp = Blueprint('play', __name__, static_folder='static', template_folder='templates')

@play_bp.route('/', methods=('GET', 'POST'))
def play():
    if request.method == 'POST':
        q_number = int(request.form['diff_button'])
        get_questions_set(q_number)
        #return redirect(url_for('play.display_question', q_number=0))
    return render_template('play.html')


@play_bp.route('qustion<int:q_number>', methods=('GET', 'POST'))
def display_question(q_number):
    current_question = session['q_set'][q_number]
    # TODO: write answer validation, score
    if q_number == len(session['q_set']) - 1:
        session.pop('q_set')
        return redirect(url_for('play.results', q_number=q_number+1))
    return redirect(url_for('play.display_question', q_number=q_number+1))


def get_questions_set(q_number):
    url = f'https://opentdb.com/api.php?amount={q_number}'
    response = requests.get(url)
    q_json = json.loads(response.text)
    data = []

    for q_info in q_json['results']:
        all_answers = [q_info['correct_answer']] + q_info['incorrect_answers']
        data.append({'correct' : q_info['correct_answer'], 'all_answers' : all_answers})

    flash(data, category='success')
    session['q_set'] = data

@play_bp.route('/results')
def display_results(q_number):
    correct = session.pop('correct')
    return render_template('result.html',correct=correct, q_number=q_number)

