from flask import Flask, request, render_template, redirect, session,Blueprint, flash, url_for,g
from werkzeug.security import check_password_hash, generate_password_hash
from pathlib import Path
import sqlite3
import os
import random


app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'database.db'

# Function to create database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create a database if it does not exist
if not Path('database.db').exists():
   with app.app_context():
     db = get_db()
     with app.open_resource('schema.sql', mode='r') as f:
         db.cursor().executescript(f.read())
     db.commit()

@app.route('/')
def home():
    return render_template('home.html')

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
            return 'Cet utilisateur existe déjà'

        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        return render_template('login.html')

    return render_template('sign.html')


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
              # Flash success message
             flash('Login successful!', 'success')
             # Assuming 'start' is the endpoint for the start page
             return render_template('start.html')
        else:
            return 'Nom d\'utilisateur ou mot de passe incorrect'

    return render_template('login.html')

# Function to retrieve a random question and its answers from the database
def get_question_and_answers():
    db = get_db()
    cursor = db.cursor()
    # Select a random question
    cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1')
    question = cursor.fetchone()
    cursor.execute('SELECT * FROM answers WHERE question_id = ?', (question['id'],))
    answers = cursor.fetchall()
    return question, answers

@app.route('/quiz')
def quiz():
    question, answers = get_question_and_answers()
    correct_answer_id = get_correct_answer_id(question['id'])
    return render_template('quiz.html', question=question, answers=answers, correct_answer_id=correct_answer_id)

def get_correct_answer_id(question_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM answers WHERE question_id = ? AND is_correct = True', (question_id,))
    correct_answer = cursor.fetchone()
    return correct_answer['id'] if correct_answer else None



if __name__ == '__main__':
    app.run(debug=True)
