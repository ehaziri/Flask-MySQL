from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app,'friends_db')
app.secret_key = 'some_secret'

#1
@app.route('/users')
def index():
    query = "SELECT * FROM friends"
    users = mysql.query_db(query)
    return render_template('index.html', all_users=users)
#2
@app.route('/users/new')
def new():
    return render_template('add.html')

#3
@app.route('/users/<id>/edit')
def edit(id):
    return render_template('edit.html', id = id)

#4
@app.route('/users/<id>')
def show(id):

    query = "SELECT * FROM friends WHERE id = :id"
    data = { 'id': id }
    specific_user = mysql.query_db(query, data)
    return render_template('show.html', this_user = specific_user)

#5
@app.route('/users/create', methods=['POST'])
def create():
    query = "INSERT INTO friends(first_name, last_name, email, created_at) VALUES (:first_name, :last_name, :email, NOW()) "
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
    }
    mysql.query_db(query, data)
    return redirect('/users')

#6
@app.route('/users/<id>/delete', methods=['POST', 'GET'])
def destroy(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = { 'id': id }
    mysql.query_db(query, data)
    flash("Successfully deleted!")
    return redirect('/users')
#7
@app.route('/users/<id>', methods=['POST'])
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
    return redirect('/users')


app.run(debug=True)
