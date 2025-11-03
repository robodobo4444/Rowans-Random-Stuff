from flask import Flask, render_template, request, redirect, url_for
import csv
import os
import secrets
from datetime import datetime

CSV_FILE = 'users.csv'
SECRET_KEY_FILE = 'secret.key'

app = Flask(__name__)
# No secret key needed if you're not using flash or sessions!

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
        # Pass error message directly to template
        return render_template("Sign_up.html", error="Username and password are required!")
    
    if username_exists(username):
        return render_template("Sign_up.html", error="That Username is in use. Please try a different one.")
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, username, password])
        # Pass success message directly to template
        return render_template("Sign_up.html", success="Account successfully created!")
    except Exception as e:
        return render_template("Sign_up.html", error=f"Error saving data: {str(e)}")

if __name__ == '__main__':
    init_csv()
    app.run(debug=True)
