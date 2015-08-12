from myapp import app, login_manager
from flask import request, render_template, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user
from datetime import datetime
import sqlite3


@app.before_first_request
def init_todos():
   execute_query('''CREATE TABLE records (date text, content text)''')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = "INSERT INTO records VALUES('%s', '%s')" % (
            datetime.now().strftime('%x'),
            request.form['content'])
        execute_query(query)
    c = execute_query('SELECT * FROM records')
    todos = c.fetchall()
    return render_template('index.html', todos=todos)


@app.route('/secret/')
@login_required
def secret():
    return render_template('secret.html')


@app.route('/search/', methods=['GET'])
def search():
    term = request.args.get('term')
    return "<html><body><h1>Search results for %s</h1>Search is " \
           "not yet supported</body></html>" % term


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        next = request.args.get('next')
        name = request.form['username']
        password = request.form['password']
        user = User(name, password)
        if user.is_valid():
            login_user(user)
            return redirect(next or url_for('index'))
        else:
            flash('Wrong login')

    return render_template('login.html')


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(userid):
    return User(userid, userid)


def execute_query(query):
    db = sqlite3.connect('todos.db')
    with db:
        return db.execute(query)

class User(object):
    def __init__(self, name, password):
        super(User, self).__init__()
        self.name = name
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name

    def get_name(self):
        return self.name

    def is_valid(self):
        return self.name == self.password
