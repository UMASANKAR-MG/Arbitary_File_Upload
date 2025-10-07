from flask import Flask, render_template, request, redirect, url_for
import os
import random
import string
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt'}
FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9]{1,200}\.[a-zA-Z0-9]{1,10}$')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename):
    # Remove any control or special characters except for alphanumeric and one dot
    filename = re.sub(r'[^a-zA-Z0-9.]', '', filename)  # Remove any unwanted characters
    # Ensure the filename matches the desired pattern (alphanumeric and one dot)
    if FILENAME_PATTERN.match(filename):
        return filename
    return None

def secure_filename(filename):
    sanitized_name = sanitize_filename(filename)
    if sanitized_name is None:
        return None
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return f"{random_str}_{sanitized_name}"


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        sanitized_filename = secure_filename(file.filename)
        if sanitized_filename is None:
            return 'Invalid file name', 400

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], sanitized_filename))
        return f'File uploaded successfully: {sanitized_filename}'

    return 'File not allowed', 400


if __name__ == '__main__':
    app.run(debug=True)

