from flask import Flask, request, redirect, render_template, session, flash
import re
from mysqlconnection import MySQLConnector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
mysql = MySQLConnector(app,'wall')
app.secret_key = 'some_secret'
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        errors = []

        if not data['first_name'] or not data['last_name'] or not data['email'] or not data['password']:
            errors.append('All fields are required')
        elif len(data['first_name']) < 2:
            errors.append('First Name must be at least 2 characters')
        elif len(data['last_name']) < 2:
            errors.append('Last Name must be at least 2 characters')
        elif not data['first_name'].isalpha():
            errors.append('First Name must contain only letters')
        elif not data['last_name'].isalpha():
            errors.append('Last Name must contain only letters')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Invalid email address')
        elif len(data['password']) < 7:
            errors.append('Password must be at least 8 characters')
        elif not data['password'] == data['confirm_password']:
            errors.append('Password and Password confirmation must match')

        if errors:
            for error in errors:
                flash(error)
        else:
            query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW()) "
            data = {
                    'first_name': request.form['first_name'],
                    'last_name': request.form['last_name'],
                    'email': request.form['email'],
                    'password': bcrypt.generate_password_hash(request.form['password'])
            }
            mysql.query_db(query, data)
            query = "SELECT id, first_name, email, password FROM users WHERE email = :email"
            user = mysql.query_db(query, data)
            session['user'] = user
            return redirect('/success')

    return render_template('register.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        query = "SELECT id, first_name, email, password FROM users WHERE email = :email"
        data = { 'email': request.form['email'] }
        user = mysql.query_db(query, data)
        if not bcrypt.check_password_hash(user[0]['password'], request.form['password']):
           flash("Please review your credentials.")
        else:
            session['user'] = user
            return redirect('/success')

    return render_template('login.html')

@app.route('/success')
def success():
    query = "SELECT users.first_name, users.last_name, users.created_at, messages.id, messages.message FROM users JOIN messages ON users.id = messages.user_id ORDER BY messages.created_at DESC"
    users_posts = mysql.query_db(query)

    qwerty = "SELECT users.first_name, users.last_name, comments.created_at, comments.comment, comments.message_id FROM users JOIN comments ON users.id = comments.user_id"
    users_comments = mysql.query_db(qwerty)

    return render_template('success.html', users_posts=users_posts, users_comments=users_comments)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/post', methods=['POST'])
def post():
    if request.form['hidden'] == 'messages':
        query = "INSERT INTO messages(user_id, message, created_at, updated_at) VALUES (:user_id, :message, NOW(), NOW())"
        data = {
                'user_id': session['user'][0]['id'],
                'message': request.form['message']
        }
        mysql.query_db(query, data)
    elif request.form['hidden'] == 'comments':
        print "Ketu"
        query = "INSERT INTO comments(message_id,user_id, comment, created_at, updated_at) VALUES (:message_id, :user_id, :comment, NOW(), NOW())"
        data = {
                'message_id': request.form['msg_id'],
                'user_id': session['user'][0]['id'],
                'comment': request.form['comment'],
        }
        print data['message_id']
        mysql.query_db(query, data)

    return redirect('/success')


app.run(debug=True)
