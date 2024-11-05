from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import ConnectDB, RandomWord
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import threading
from utils import RandomWord, ConnectDB
from turbo_flask import Turbo
import time
import random

database = 'instance/db.sqlite3'
datatable = 'WORDS'
dailytable = 'daily_words'

db_1 = ConnectDB(database)
data1 = db_1.connect_to_db(datatable)

class StoreData():
    state = False #  
    table = []
    test_table = []
    
    def start(self):
        self.state = False
    
    def stop(self):
        self.state = True
    
    def getTestTable(self):
        if not self.test_table:
            self.test_table = self.table.copy()
            
    def test(self):
        data = random.choice(self.test_table)
        _, word, _ = data
        index = self.test_table.index(data)
        self.test_table.pop(index)
        return word
    
    def pop(self, index):
        self.test_table.pop(index)

daily_storage = StoreData()

# create flask app
app = Flask(__name__)
turbo = Turbo(app)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Word data
@app.context_processor  
def daily_word_data():
    daily_word = RandomWord(database, datatable)
    daily_word.random_database()
    daily_data = db_1.connect_to_db(dailytable)  
    data_list = daily_data.copy()
    daily_storage.table = data_list
    return {'d_word': data_list}

def update():
    with app.app_context():
        while True:
            turbo.push(turbo.replace(render_template('daily_data.html'), 'up'))
            time.sleep(60)

th = threading.Thread(target=update, )
th.daemon = True
th.start()

# secret key
app.config['SECRET_KEY'] = 'my-secret-key' # need to be modified later

# Initialisze the db
db = SQLAlchemy(app)

# Create user Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    def  __repr__(self):
        return '<Name %r>' % self.user_name

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader callback
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(int(user_id))

# Login 
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        user =  Users.query.filter_by(user_name=_username).first()
        if user:
            if bcrypt.checkpw(_password.encode('utf-8'), user.password):
                login_user(user)
                if 'score' in session:
                    session.pop('score')
                return redirect(url_for('dashboard'))
            else:
                error = "pw-error"
        else:
            error = "user-error"
    return render_template('login.html', error=error)

# Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out!')
    return redirect(url_for('login'))

# Registration 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        _email = request.form['email']
        user_mail = Users.query.filter_by(email=_email).first()
        if user_mail is None:
            _user_name = request.form['user_name']
            user_name = Users.query.filter_by(user_name=_user_name).first()
            if user_name is None:
                _password = request.form['password']
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(_password.encode('utf-8'), salt)
                user = Users(user_name=_user_name, email=_email, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash("*Username alreay used.", "error")
        else:
            flash("*Email alreay used.", "error")
    return render_template('register.html')

# restor password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return 'Reset password page'


@app.route('/data')
def data():
    if 'score' in session:
        session.pop('score')
    return render_template('data_.html', data=data1)

@app.route('/daily_data')
def daily_data():
    if 'score' in session:
        session.pop('score')
    return render_template('data.html')

@app.route('/home')
@login_required
def home():
    if 'score' in session:
        session.pop('score')
    return render_template('home.html')

@app.route('/test')
@login_required
def test():
    if 'score' not in session:
        daily_storage.getTestTable()
        if not daily_storage.state:
            session['score'] = 0
    temp = daily_storage.test_table
    if temp:
        word = daily_storage.test()
        session['current_word'] = word
        return render_template('test_page.html', word=word)
    else:
        return redirect('score')

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    score = session['score']
    submitted_answer = request.form['answer']
    current_word = session.get('current_word')
    if submitted_answer == current_word:
        session['score'] = score +1   
    return redirect('/test')

@app.route('/score')
@login_required
def score():
    if 'score' in session:
        score = session['score']
        session['score'] = 0
        session.pop('score')
        return render_template('score.html', score=score)
    else:
        return redirect('/test')
    

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if 'score' in session:
        session.pop('score')
    return render_template('dashboard.html')

@app.route('/library')
@login_required
def library():
    return render_template("library.html")



if __name__ == "__main__":
        app.run(debug=True)