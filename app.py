from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    user__name = "robodobo4444"
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

if __name__ == '__main__':
    app.run(debug=True)
