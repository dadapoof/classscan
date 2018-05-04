from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Students
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'classscan'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

Students = Students()

# Index
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
def home():
    return render_template('index.html')


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


# User Register
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


# User login
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('administrator.html'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login.html'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login.html'))


# studentForm Class
class StudentForm(Form):
    name = StringField('name', [validators.Length(min=1, max=200)])
    classroom = StringField('classroom', [validators.Length(max=10)])



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)