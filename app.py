from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime


CSV_FILE = 'users.csv'
app = Flask(__name__)
def init_csv():
       if not os.path.exists(CSV_FILE):
           with open(CSV_FILE, 'w', newline='') as f:
               writer = csv.writer(f)
               writer.writerow(['Timestamp', 'Username', 'Password'])

@app.route('/')
def home():
    user_name = ""
    return render_template('index.html', name = user_name)

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
def sign_up():
    return render_template("Sign_up.html")
@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, 'r') as f:
        if username in f.read():
            username_in_use = True
        else:
            username_in_use = False
    if username_in_use == False:
        try:
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, username, password])
    
            flash('Data successfully saved!', 'success')
        except Exception as e:
            flash(f'Error saving data: {str(e)}', 'error')
    if username_in_use == True:
        flash("That Username is in use, Please try a different one", 'message')

    return redirect('Sign_up.html')


if __name__ == '__main__':
    init_csv()
    app.run(debug=True)
