from flask import Flask, render_template, request, flash
import csv
import os
import secrets
from datetime import datetime

CSV_FILE = 'users.csv'
SECRET_KEY_FILE = 'secret.key'

app = Flask(__name__)

# Generate or load secret key
def get_or_create_secret_key():
    if os.path.exists(SECRET_KEY_FILE):
        with open(SECRET_KEY_FILE, 'r') as f:
            return f.read().strip()
    else:
        key = secrets.token_hex(32)
        with open(SECRET_KEY_FILE, 'w') as f:
            f.write(key)
        return key

app.secret_key = get_or_create_secret_key()

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Username', 'Password'])

def username_exists(username):
    if not os.path.exists(CSV_FILE):
        return False
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Username'] == username:
                return True
    return False

@app.route('/')
def home():
    user_name = ""
    return render_template('index.html', name=user_name)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/small_projects')
def small_projects():
    return render_template('small_projects.html')

@app.route('/major_projects')
def major_projects():
    return render_template('major_projects.html')

@app.route("/Sign_up")
def Sign_up():
    return render_template("Sign_up.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        flash("Username and password are required!", 'error')
        return render_template("Sign_up.html")
    
    if username_exists(username):
        flash("That Username is in use. Please try a different one.", 'error')
        return render_template("Sign_up.html")
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, username, password])
        flash('Account successfully created!', 'success')
    except Exception as e:
        flash(f'Error saving data: {str(e)}', 'error')
    
    return render_template("Sign_up.html")

if __name__ == '__main__':
    init_csv()
    app.run(debug=True)
