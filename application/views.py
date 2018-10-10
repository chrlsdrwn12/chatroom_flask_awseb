from application import app, socketio
from flask import render_template, jsonify, request, redirect, url_for, session, flash, json
import os, datetime, time
from functools import wraps
from flask_socketio import send, emit


# set the secret key for session.  keep this really secret:
app.secret_key = 'A0Zr98j/3ysX R~XhHkH!jLWX/,?RT'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def validateUser(username, password):
    users = ''
    with open('app.json', encoding='utf-8') as data_file:
        data = json.load(data_file)
        users = data['users']
    userinfo = search(username, users)
    if userinfo and password == userinfo[0]['password']:
        print(userinfo)
        return userinfo[0]
    return False

@app.route("/")
@login_required
def home():
    alias = '%s' % session['alias']
    username = '%s' % session['username']
    return render_template('index.html', **locals())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = validateUser(username, password)
        if user:
            session['username'] = user['username']
            session['alias'] = user['alias']
            return redirect(url_for('home'))
        else:
            flash("Incorrect login.")
    return render_template('login.html')

def search(name, people):
    return [element for element in people if element['username'] == name]

@socketio.on('public_msg', namespace='/messages')
def receive_public_msg(message):
    # print('USER MESSAGE: {}'.format(message))
    emit('public_msg_res', 
        message, 
        broadcast=True
    )

@app.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out.")
    return redirect(url_for('login'))