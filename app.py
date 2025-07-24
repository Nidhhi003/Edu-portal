
from flask import Flask, render_template, request, redirect, send_from_directory
from flask import flash, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


app = Flask(__name__)
app.secret_key = '1234'  # ← Add this near the top

app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    with sqlite3.connect('database.db') as conn:
        with open('schema.sql') as f:
            try:
             conn.executescript(f.read())
            except sqlite3.OperationalError:
                pass  # Table already exists, ignore error


@app.route('/')
def index():
    print("SESSION:", session) 
    if 'user_id' not in session:
        return redirect('/register')
    return render_template('index.html')  # ← your real homepage after login


@app.route('/overview')
def overview():
    if 'user_id' not in session:
     return redirect('/login')
    return render_template('overview.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        file = request.files['file']
        subject = request.form['subject']
        user_id = session.get('user_id')
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            conn = sqlite3.connect('database.db')
            conn.execute("INSERT INTO files (filename, subject, user_id) VALUES (?, ?, ?)", (filename, subject, user_id))
            conn.commit()
            conn.close()
            return redirect('/files')
    return render_template('upload.html')
    


@app.route('/files')
def files():
    if 'user_id' not in session:
        return redirect('/login')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM files")
    files = cur.fetchall()
    conn.close()
    return render_template('files.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    if 'user_id' not in session:
        return redirect('/login')

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    user_id = session.get('user_id')
    if 'user_id' not in session:
        return redirect('/login')

    if not user_id:
        return "Unauthorized"

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM files WHERE filename = ?", (filename,))
    result = cur.fetchone()
    if result and result[0] == user_id:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        conn.execute("DELETE FROM files WHERE filename = ?", (filename,))
        conn.commit()
    conn.close()
    return redirect(url_for('files'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])  # hashing
        conn = sqlite3.connect('database.db')
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template('auth.html', register_error="Username already exists", show_login=False)
        conn.close()
        return redirect('/login')
    return render_template('auth.html', show_login=False)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        result = cur.fetchone()
        conn.close()

        print("Fetched from DB:", result)

        if result and check_password_hash(result[1], password):
            session['user_id'] = result[0]
            session['username'] = username
            print("Login success")
            return redirect('/')
        else:
            print("Login failed")
            return render_template('auth.html', login_error="Invalid username or password", show_login=True)

    return render_template('auth.html', show_login=True)






@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
