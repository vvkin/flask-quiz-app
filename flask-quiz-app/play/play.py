from flask import Blueprint, g, render_template, request, redirect, flash, url_for, session
import requests

play_bp = Blueprint('play', __name__, static_folder='static', template_folder='templates')

@play_bp.route('/', methods=('GET', 'POST'))
def play():
    if request.method == 'POST':
        q_number = int(request.form['diff_button'])
        get_questions_set(q_number)
        return redirect(url_for('play.display_question', q_number=0))
    return render_template('play.html')


@play_bp.route('/question/<int:q_number>/', methods=('GET', 'POST'))
def display_question(q_number):
    if request.method == 'POST':
        answer = request.form['answer']
        flash(answer + ' ' + session['q_set'][q_number]['correct'])
        if answer == session['q_set'][q_number]['correct']:
           session['c_answ'] += 1
        return redirect(url_for('play.display_question', q_number=q_number+1))

    if q_number == len(session['q_set']):
        return redirect(url_for('play.display_results'))
    
    current_question = session['q_set'][q_number]
    return render_template('question.html', question=current_question)


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
    session['c_answ'] = 0

@play_bp.route('/results')
def display_results():
    q_number = len(session.pop('q_set'))
    c_number = session.pop('c_answ')
    return render_template('results.html',c_number=c_number, q_number=q_number)

