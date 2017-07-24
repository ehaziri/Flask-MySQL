from flask import Flask, render_template, request, redirect
from connection import MySQLConnector
app = Flask(__name__)

db = MySQLConnector(app, 'friends_db')

# DB QUERIES
queries = {
    'index' : "SELECT * FROM friends",
    'create' : "INSERT INTO friends (first_name, last_name, email, created_at) VALUES (:first_name, :last_name, :email, NOW())",
    'show' : "SELECT * FROM friends WHERE id = :id",
    'update' : "UPDATE friends SET first_name=:first_name, last_name = :last_name, email=:email WHERE id = :id",
    'delete' : "DELETE FROM friends WHERE id = :id"
}

# ROUTING
@app.route('/')
def index():
    query = queries['index']
    data = {}
    friends = db.query_db(query, data)
    return render_template('index.html', friends=friends)

@app.route('/friends', methods=["POST"])
def create():
    query = queries['create']
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email']
    }
    db.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>', methods=["POST"])
def update(id):
    query = queries['update']
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'id' : id
    }
    db.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/edit', methods=["GET"])
def edit(id):
    query = queries['show']
    data = {
        'id': id
    }
    friend = db.query_db(query, data)[0]
    return render_template('edit.html', friend=friend )

@app.route('/friends/<id>/delete', methods=["POST"])
def delete(id):
    query = queries['delete']
    data = {
        'id' : id
    }
    db.query_db(query, data)
    return redirect('/')

app.run(debug=True)
Privacy Policy
