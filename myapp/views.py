from myapp import app, login_manager
from flask import request, render_template, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user
from datetime import datetime

todos = list()


@app.before_first_request
def init_todos():
    global todos
    todos.append({'date': datetime.now().strftime('%x'),
                  'content': 'important news'})


@app.route('/', methods=['GET', 'POST'])
def index():
    global todos
    if request.method == 'POST':
        todos.append({'date': datetime.now().strftime('%x'),
                      'content': request.form['content']})
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
