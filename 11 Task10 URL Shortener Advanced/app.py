from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.secret_key = "wasiq"

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urlshorten.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ MODELS ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(50), unique=True, nullable=False)

# ------------------ ROUTES ------------------

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/dashboard')
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('signup'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            session['username'] = user.username
            return redirect('/dashboard')

        return render_template('index.html', error="Invalid username or password")

    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('dashboard.html')


@app.route('/shortener', methods=['GET', 'POST'])
def shortener():
    if request.method == 'POST':
        original_url = request.form.get('original_url')

        if not original_url:
            flash("URL is required")
            return redirect(url_for('dashboard'))

        short_url = generate_url()
        url = Url(original_url=original_url, short_url=short_url)

        db.session.add(url)
        db.session.commit()

        return render_template(
            'dashboard.html',
            short_url=request.host_url + short_url
        )

    return render_template('dashboard.html')


@app.route('/<short_url>')
def redirect_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url.original_url)


@app.route('/urls')
def urls():
    urls = Url.query.all()
    return render_template('urls.html', urls=urls)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# ------------------ HELPERS ------------------

def generate_url():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))


# ------------------ RUN ------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # creates SQLite tables automatically
    app.run(debug=True)
