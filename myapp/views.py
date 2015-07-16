from myapp import app, login_manager
from flask import request, render_template, redirect, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/secret/')
@login_required
def secret():
    return render_template('secret.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # do the login
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
