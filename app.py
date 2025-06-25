
from flask import Flask, render_template, request, redirect, send_from_directory
from flask import flash, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    with sqlite3.connect('database.db') as conn:
        with open('schema.sql') as f:
            conn.executescript(f.read())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        subject = request.form['subject']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            conn = sqlite3.connect('database.db')
            conn.execute("INSERT INTO files (filename, subject) VALUES (?, ?)", (filename, subject))
            conn.commit()
            conn.close()
            return redirect('/files')
    return render_template('upload.html')

@app.route('/files')
def files():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM files")
    files = cur.fetchall()
    conn.close()
    return render_template('files.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)

        # Remove from DB
        conn = sqlite3.connect('database.db')
        conn.execute("DELETE FROM files WHERE filename = ?", (filename,))
        conn.commit()
        conn.close()

    return redirect(url_for('files'))




if __name__ == '__main__':
    init_db()
    app.run(debug=True)
