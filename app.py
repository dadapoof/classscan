from flask import Flask, render_template
from data import Students

app = Flask(__name__)

Students = Students()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/index.html')
def home():
	return render_template('index.html')

@app.route('/ask.html')
def ask():
	return render_template('ask.html')

@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/signup.html')
def signup():
	return render_template('signup.html')

@app.route('/administrator.html')
def students():
	return render_template('administrator.html', students = Students)

@app.route('/administrator/<string:id>/')
def student(id):
	return render_template('administrator.html', id=id)

if __name__ == '__main__':
	app.run(debug=True)