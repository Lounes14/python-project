from flask import Flask, request, render_template, redirect, session,Blueprint, flash, url_for,g
from werkzeug.security import check_password_hash, generate_password_hash
from pathlib import Path
import sqlite3
import os
import random


app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'database.db'

# Fonction pour créer la connexion à la base de données
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
# Crée une base de données si elle existe pas

if not Path('database.db').exists():
   with app.app_context():
     db = get_db()
     with app.open_resource('schema.sql', mode='r') as f:
         db.cursor().executescript(f.read())
     db.commit()

@app.route('/')
def home():
    return "<p>Bienvenue sur votre site !</p><p><a href='/sign'>S'inscrire</a></p><p><a href='/login'>Se connecter</a></p>"

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
        return 'Inscription réussie'

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
            return 'Connexion réussie'
        else:
            return 'Nom d\'utilisateur ou mot de passe incorrect'

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
