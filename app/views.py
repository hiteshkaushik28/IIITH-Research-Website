# Views are handlers that responds to requests from browsers and clients

# Handlers are written as Python Functions. 

# Each View Function is mapped to one or more request URLs.

from flask import render_template, flash, redirect, url_for, session, logging, request
from app import app
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/bhavidhingra/google-drive-iiith/Semester_#1/CSE505 : Scripting & Computer Environments/Projects/IIITH-Research-Website/database/iiith_research.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Articles(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	author = db.Column(db.String(50))
	body = db.Column(db.Text)
	date_posted = db.Column(db.DateTime)


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	email = db.Column(db.String(50))
	username = db.Column(db.String(30))
	password = db.Column(db.String(50))
	register_date = db.Column(db.DateTime)


# class Professor(db.Model):
# 	id

# Index
@app.route('/')
@app.route('/index')
def home():
	return render_template('home.html')


# About
@app.route('/about')
def about():
	return render_template('about.html')


# Articles
@app.route('/articles')
def articles():
	articles = Articles.query.order_by(Articles.date_posted.desc()).all()

	if len(articles) > 0:
		return render_template('articles.html', articles=articles)
	else:
		msg = 'No Articles Found'
		return render_template('articles.html', msg=msg)


# Single Article
@app.route('/article/<string:id>')
def article(id):
	# Get article using 'id'
	article = Articles.query.get(id)
	return render_template('article.html', article=article)


# Register Form Class
class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		# Create new user
		user = Users(name=name, email=email, username=username, password=password, register_date=datetime.now())

		# Add user to database
		db.session.add(user)
		db.session.commit()

		flash('You are now registered and can log in', 'success')
		return redirect(url_for('register'))

	return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		# Get Form Fields
		username = request.form['username']
		password_candidate = request.form['password']
		category = request.form['category']

		user = Users.query.filter_by(username=username).first()

		if user is not None:
			# Get stored hash
			password = user.password

			# Compare Passwords
			if sha256_crypt.verify(password_candidate, password):
				# Passed
				session['logged_in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')
				if category == "Professor":
					return redirect(url_for('professor'))
				else:
					return redirect(url_for('student'))

				# return redirect(url_for('dashboard'))
			else:
				error = 'Invalid login'
				return render_template('login.html', error=error)
		else:
			error = 'Username not found'
			return render_template('login.html', error=error)

	return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('home'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	articles = Articles.query.all()

	if len(articles) > 0:
		return render_template('dashboard.html', articles=articles)
	else:
		error = 'No Articles Found'
		return render_template('dashboard.html', error=error)
	

# Professor
@app.route('/professor')
@is_logged_in
def professor():
	# articles = Articles.query.all()

	# if len(articles) > 0:
	# return render_template('professor.html', articles=articles)
	return render_template('professor.html')
	# else:
	# 	error = 'No Articles Found'
	# 	return render_template('dashboard.html', error=error)


# Student
@app.route('/student')
@is_logged_in
def student():
	return render_template('student.html')


# Article Form Class
class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=200)])
	body = TextAreaField('Body', [validators.Length(min=30)])
	

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		body = form.body.data
		author = session['username']

		# Create new user
		article = Articles(title=title, author=author, body=body, date_posted=datetime.now())

		# Add user to database
		db.session.add(article)
		db.session.commit()

		flash('Article Created', 'success')
		return redirect(url_for('dashboard'))
	
	return render_template('add_article.html', form=form)


# # Edit Article
# @app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
# @is_logged_in
# def edit_article(id):
# 	# Create cursor
# 	cur = mysql.connection.cursor()

# 	# Get article by id
# 	result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

# 	article = cur.fetchone()

# 	# Get form
# 	form = ArticleForm(request.form)

# 	# Populate article from fields
# 	form.title.data = article['title']
# 	form.body.data = article['body']


# 	if request.method == 'POST' and form.validate():
# 		title = request.form['title']
# 		body = request.form['body']

# 		# Create Cursor
# 		cur = mysql.connection.cursor()

# 		# Execute
# 		cur.execute("UPDATE articles SET title = %s, body = %s WHERE id = %s", (title, body, id))

# 		# Commit to DB
# 		mysql.connection.commit()

# 		# Close connection
# 		cur.close()

# 		flash('Article Updated', 'success')
# 		return redirect(url_for('dashboard'))
	
# 	return render_template('edit_article.html', form=form)



# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
	article = Articles.query.get(id)
	db.session.delete(article)
	db.session.commit()
	flash('Article Deleted', 'success')

	return redirect(url_for('dashboard'))