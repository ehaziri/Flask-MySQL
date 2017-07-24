# DEPENDECIES
from flask import Flask, render_template, request, redirect, flash
from mysqlconnection import MySQLConnector
import re

# APP, DB, CONSTANTS
app = Flask(__name__)
mysql = MySQLConnector(app, 'email_validation')
EMAIL_REGEX = re.compile(r'^[\w\.+_-]+@[\w\._-]+\.[\w]*$')
app.secret_key = 'some_secret'

# SQL QUERIES
queries = {
    'create' : "INSERT INTO emails (email, created_at) VALUES (:email, NOW());",
    'index' : "SELECT * FROM emails",
    'delete' : "DELETE FROM emails WHERE id = :id"
}


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Logic that (1) tests whether an email is valid, (2) if so, adds it to DB
        if(validateEmail(request.form['email'])):
            query = queries['create']
            data = { 'email' : request.form['email'] }
            mysql.query_db(query, data)
            flash('Successfully created email record!')
            return redirect('/success')
        else:
            # Email isn't valid, flash an error message
            flash('Not a valid email!')

    return render_template('index.html')

@app.route('/success', methods=["GET"])
def success():
    query = queries['index']
    data = {}
    emails = mysql.query_db(query, data)
    return render_template('success.html', emails=emails)

@app.route('/<id>', methods=["POST"])
def destroy(id):
    query = queries['delete']
    data = {
        'id' : id
    }
    flash('Successfully deleted email!')
    mysql.query_db(query, data)
    return redirect('/success')

def validateEmail(email):
    # Return whether or not the email passed in is valid
    return EMAIL_REGEX.match(email)

app.run(debug=True)
