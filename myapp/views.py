from xml.sax import SAXParseException
from myapp import app, login_manager
from flask import request, render_template, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user, \
    current_user
from datetime import datetime
import sqlite3
from parser import TODOListHandler


@app.before_first_request
def init_todos():
    execute_query('''CREATE TABLE IF NOT EXISTS records (date text, content text,
    owner text)''')


def add_todo(date, content, owner):
    query = "INSERT INTO records VALUES('%s', '%s', '%s')" % \
            (date, content, owner)
    execute_query(query)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        add_todo(datetime.now().strftime('%x'),
                 request.form['content'],
                 current_user.name)

    c = execute_query("SELECT * FROM records WHERE owner='%s'" %
                      current_user.name)
    todos = c.fetchall()
    return render_template('index.html', todos=todos)


@app.route('/secret/')
@login_required
def secret():
    return render_template('secret.html')


@app.route('/uploader/', methods=['POST'])
@login_required
def uploader():
    import xml.sax
    p = TODOListHandler()
    try:
        xml.sax.parse(request.files['file'], p)
        for it in p.get_todos():
            add_todo(it[0], it[1], current_user.name)
    except SAXParseException:
        flash('Unable to parse file')

    return redirect(url_for('index'))


@app.route('/search/', methods=['GET'])
def search():
    term = request.args.get('term')
    query = "SELECT * FROM records WHERE content LIKE '%%%s%%'" % term
    print "Executing %s" % query
    res = execute_query(query)
    return "<html><body><h1>Search result for %s</h1>%s</body></html>" % (
        term, res.fetchall())


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
