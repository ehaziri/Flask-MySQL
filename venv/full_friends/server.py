from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app,'friends_db')
app.secret_key = 'some_secret'

@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends)

@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friends(first_name, last_name, email, created_at) VALUES (:first_name, :last_name, :email, NOW()) "
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
    }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/edit', methods=['POST'])
def edit(id):
    return render_template('edit.html', id = id)

@app.route('/friends/<id>', methods=['POST'])
def update(id):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email, created_at = NOW() WHERE id = :id"
    data = {
            'id' : id,
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email']
    }
    mysql.query_db(query, data)
    flash("Successfully updated!")
    return redirect("/")

@app.route('/friends/<id>/delete', methods=["POST"])
def destroy(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = { 'id': id }
    mysql.query_db(query, data)
    flash("Successfully deleted!")
    return redirect('/')



app.run(debug=True)
