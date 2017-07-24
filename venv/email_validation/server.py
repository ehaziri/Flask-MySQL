from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app,'email_validation')
app.secret_key = 'some_secret'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if len(request.form['email']) < 1 or not EMAIL_REGEX.match(request.form['email']):
            flash("Email is not valid!")
        else:
            data = { 'email' : request.form['email'] }
            query = "INSERT INTO emails(email, created_at) VALUES (:email, NOW());"
            mysql.query_db(query, data)
            flash("The email address you entered: {}, is a valid email address! Thank you!".format(request.form['email']))
            return redirect('/success')

    return render_template('index.html')

@app.route('/success')
def success():
    query = "SELECT * FROM emails;"
    emails = mysql.query_db(query)
    return render_template("success.html", all_emails=emails)

@app.route('/<id>', methods=['POST'])
def delete(id):
    query = "DELETE FROM emails WHERE id = :id"
    data = { 'id': id }
    mysql.query_db(query, data)
    flash("Deleted email!")
    return redirect('/success')

app.run(debug=True)
