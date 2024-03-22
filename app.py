from flask import Flask, request, redirect, flash, url_for, g, session, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from pathlib import Path
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'database.db'

# Function to create a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Close the database connection at the end of the request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create the database if it does not exist
if not Path('database.db').exists():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Sign-up page
@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return 'This user already exists'

        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        return render_template('login.html')

    return render_template('sign.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            flash('Login successful!', 'success')
            return render_template('start.html')
        else:
            return 'Incorrect username or password'

    return render_template('login.html')

# User logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))

# Function to retrieve a random question and its answers from the database
def get_question_and_answers():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1')
    question = cursor.fetchone()
    cursor.execute('SELECT * FROM answers WHERE question_id = ?', (question['id'],))
    answers = cursor.fetchall()
    return question, answers

# Quiz page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():

    if request.method == 'POST':
        selected_answer_id = request.form.get('answer')
        correct_answer_id = get_correct_answer_id(request.form.get('question_id'))

        if selected_answer_id == correct_answer_id:
            session['score'] += 1

        session['answered_questions'] += 1

        if session['answered_questions'] >= 5:
            session['played_game'] = True
            session['answered_questions'] = 0  # Reset the answered_questions count
            return redirect(url_for('end'))

    question, answers = get_question_and_answers()
    correct_answer_id = get_correct_answer_id(question['id'])
    return render_template('quiz.html', question=question, answers=answers, correct_answer_id=correct_answer_id)



# Function to retrieve the ID of the correct answer
def get_correct_answer_id(question_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM answers WHERE question_id = ? AND is_correct = True', (question_id,))
    correct_answer = cursor.fetchone()
    return correct_answer['id'] if correct_answer else None

# Score page
@app.route('/end')
def score():

    # Récupérer le score total depuis les paramètres de l'URL
    final_score = request.args.get('score', default=0, type=int)

    return render_template('end.html', final_score=final_score)


# Restart the quiz
@app.route('/replay', methods=['GET'])
def replay():

    # Remove the score and answeredQuestions stored in the session
    session.pop('score', None)
    session.pop('answeredQuestions', None)

    # Redirect to the quiz page to restart the game
    return redirect(url_for('quiz'))


if __name__ == '__main__':
    app.run(debug=True)
