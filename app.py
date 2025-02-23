
from flask import Flask, render_template, request, jsonify
from arduino_config import read_card
from database import add_user, get_user_by_code
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
DB_FILE = 'database.db'
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scan', methods=['GET'])
def scan_card():
    """API to scan an RFID/NFC card"""
    code = read_card()
    return jsonify({'code': code if code else None})


@app.route('/submit', methods=['POST'])
def submit_form():
    """API to submit card data"""
    form_data = request.json
    code = form_data.get('code')
    name = form_data.get('name')
    year = form_data.get('year')
    section = form_data.get('section')
    dept = form_data.get('dept')
    role = form_data.get('role')  # Adding role (student/teacher)

    if get_user_by_code(code):
        return jsonify({'status': 'error', 'message': 'Card already registered!'})

    success = add_user(code, name, year, section, dept, role)
    if success:
        return jsonify({'status': 'success', 'message': 'Data saved successfully!'})
    else:
        return jsonify({'status': 'error', 'message': 'Error saving data!'})


@app.route('/view')
def view_data():
    """Fetch and display all registered RFID card data in a table"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('view.html', users=users)


@app.route('/upload_notice', methods=['GET', 'POST'])
def upload_notice():
    """Upload a notice image"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return jsonify({'status': 'success', 'message': 'Notice uploaded!', 'file_path': file_path})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid file type'})
    
    return render_template('upload_notice.html')


if __name__ == '__main__':
    app.run(debug=True)