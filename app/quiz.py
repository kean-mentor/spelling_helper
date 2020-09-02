from flask import Blueprint, redirect, render_template, request, session, url_for

import sqlalchemy

from .import db
from .models import Score, Word
from .utils import check_answer, prepare_question


bp = Blueprint("quiz", __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # Prepare session variables
        session.clear()
        session['available_words'] = [word.value for word in Word.query.all()]
        session['username'] = request.form.get('username')
        session['total'] = int(request.form.get('total'))
        session['question_ids'] = []
        session['score'] = 0

        if session['total'] > len(session['available_words']):
            return redirect(url_for('quiz.list_words'))

        # Start quiz
        return redirect(url_for('quiz.exam'))

@bp.route('/exam', methods=['GET', 'POST'])
def exam():
    if request.method == 'POST':
        answer = request.form.get('answer')
        if check_answer(session['question'], answer):
            session['score'] += 1

        session['question_nr'] += 1

        if session['question_nr'] > session['total']:
            return redirect(url_for('quiz.result'))

    if 'question_nr' not in session:
        session['question_nr'] = 1

    question = prepare_question(session['available_words'], session['question_ids'])
    session['question'] = question
    session['question_ids'].append(question['a'])

    data = {}
    data['total'] = session['total']
    data['question'] = question
    data['current'] = session['question_nr']

    return render_template('exam.html', data=data)

@bp.route('/result')
def result():
    data = {}
    data['username'] = session['username']
    data['score'] = session['score']
    data['percent'] = (session['score'] / session['total']) * 100

    if 'result_saved' not in session:
        score = Score(
            username=data['username'],
            score=data['score'],
            percent=data['percent']
        )
        db.session.add(score)
        db.session.commit()
        session['result_saved'] = True if score.score_id else False

    top_scores = Score.query.order_by(Score.percent.desc()).limit(5).all()
    data['top'] = top_scores

    return render_template('result.html', data=data)


@bp.route('/words')
def list_words():
    words = Word.query.order_by(Word.value).all()
    return render_template('words.html', words=words)

@bp.route('/word/create', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        value = request.form.get('value')

        if 'j' in value or 'ly' in value:
            word = Word(value=value)
            try:
                db.session.add(word)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                db.session.rollback()

            return redirect(url_for('quiz.list_words'))

    return render_template('create.html')

@bp.route('/word/<int:word_id>/delete')
def delete_word(word_id):
    word = Word.query.get(word_id)

    if word:
        db.session.delete(word)
        db.session.commit()

    return redirect(url_for('quiz.list_words'))
