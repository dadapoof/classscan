from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Students
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Configuration of MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dadapoof$'
app.config['MYSQL_DB'] = 'classscan'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initializing MYSQL
mysql = MySQL(app)

Students = Students()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/index.html')
def home():
	return render_template('index.html')

@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/administrator.html')
def students():
	return render_template('administrator.html' students = Students)

@app.route('/administrator/<string:id>/')
def student(id):
	return render_template('administrator.html', id=id)

class RegisterForm(Form):
	school_name = StringField('School', [validators.Length(min=1, max=200)])
	school_address = StringField('School Address', [validators.Length(min=5, max=250)])
	school_phone = StringField('School Phone', [validators.Length(min=10, max=10)])
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=50)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
		])
	confirm = PasswordField('Confirm Password')

@app.route('/ask.html', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		school_name = form.school_name.data
		school_address = form.school_address.data
		school_phone = form.school_phone.data
		name = form.name.data
		username = form.username.data
		email = form.email.data
		password = sha256_crypt.encrypt(str(form.password.data))

		# Creating the cursor
		# Allows connection to MYSQL
		cur = mysql.connection.cursor()

		# Execute Query
		cur.execute("INSERT INTO users(school_name, school_address, school_phone, name, username, email, password) VALUES(%s, %s, %s, %s, %s, %s, %s)", (school_name, school_address, school_phone, name, username, email, password))

		# Commit to the DATABASE
		mysql.connection.commit()

		# Closing the connection
		cur.close()

		flash('Congrats! You are now registered to ClassScan and can log in!', 'success')

		return redirect(url_for('login'))
	return render_template('ask.html', form=form)


if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)