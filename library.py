from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.secret_key =os.environ.get('SECRET_KEY', 'thedaysofthejaguar')

def init_db():
	conn = sqlite3.connect('users.db')
	cur = conn.cursor()
	cur.execute('''
	CREATE TABLE IF NOT EXISTS
	users(
	id INTEGER PRIMARY KEY
	AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
	)
	''')
	conn.commit()
	conn.close()

init_db()

@app.route('/')
def home():
	if 'user' in session:
		return redirect(url_for('library'))
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        
        conn = None
        try:
            # Use context manager for auto-commit/rollback and connection cleanup
            with sqlite3.connect('users.db', timeout=20) as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                conn.commit()  # Explicit commit (optional but good practice)
                flash("Registered successfully! Please log in.")
                return redirect(url_for('login'))

        except sqlite3.IntegrityError:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        except Exception as e:
            flash(f'Registration failed: {str(e)}')
            return redirect(url_for('register'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method =="POST":
		username = request.form['username']
		password = request.form['password']
		
		conn = None
		try:
			conn = sqlite3.connect('users.db', timeout =20)
			cur = conn.cursor()
			cur.execute('SELECT password FROM users WHERE username = ?', (username,))
			user = cur.fetchone()
		finally:
			if conn:
				conn.close()
		
		if user and check_password_hash(user[0], password):  # Fixed variable name
		    session['user'] = username
		    return redirect(url_for('library'))
		else:
			flash('Invalid credentials')
			return redirect(url_for('login'))
		
	return render_template('login.html')

@app.route('/library')
def library():
	if 'user' in session:
	    return render_template('library.html')
	else:
		return redirect(url_for('login'))
		
@app.route('/menu')
def menu():
	if 'user' in session:
		return render_template('menu.html')
	else:
		return redirect(url_for('library'))
		
@app.route('/converter')
def converter():
		if 'user' in session:
			return render_template('Text to speech converter.html')
		else:
		    return redirect(url_for('library'))
		
@app.route("/photo")
def photo():
		if 'user' in session:
		    return render_template('Photo editor.html')
		else:
			return redirect(url_for('library'))

@app.route('/weather')
def weather():
		if 'user' in session:
			return render_template('Weather.html')
		else:
			return redirect(url_for('library'))
			
@app.route('/Tracker')
def tracker():
		if 'user' in session:
			return render_template('Tracker.html')
		return redirect(url_for('library'))
		
@app.route('/Scanner')
def scanner():
		if 'user' in session:
			return render_template('QR scanner.html')
		return redirect(url_for('library'))
		
@app.route('/Generator')
def generator():
		if 'user' in session:
			return render_template('QR generator.html')
		return redirect(url_for('library'))
		
@app.route('/logout')
def logout():
	session.pop('user', None)
	flash('Logged out successfully.')
	return redirect(url_for('login'))
	
if (__name__) =='__main__':
	app.run(port=8000, debug=True)