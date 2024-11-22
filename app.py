from flask import Flask, render_template, request, redirect
import bcrypt
import sqlite3


app = Flask(__name__)

def create_connection():
    conn = sqlite3.connect('Data.db')
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username TEXT NOT NULL, email TEXT NOT NULL,password TEXT NOT NULL)")
    conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        if user_data:
            hashed_password = user_data[3]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return redirect('/')
            else:
                return render_template('login.html', error='Invalid password')
        else:
            return render_template('login.html', error='Invalid username')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        return redirect('/login')
    return render_template('register.html')

if __name__ == '__main__':
    conn = create_connection()
    create_table(conn)
    app.run(debug=True)