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
from sqlalchemy_utils import EmailType
from operator import attrgetter


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/bhavidhingra/google-drive-iiith/Semester_#1/CSE505 : Scripting & Computer Environments/Projects/IIITH-Research-Website/database/iiith_research.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student_likes_Publications(db.Model):
	__tablename__ = 'student_likes_publications'
	tempid = db.Column(db.Integer, primary_key=True)
	rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))
	publicationid = db.Column(db.Integer,db.ForeignKey('publications.id', onupdate='CASCADE', ondelete='CASCADE'))

class Professor_likes_Publications(db.Model):
	__tablename__ = 'professor_likes_publications'
	tempid = db.Column(db.Integer, primary_key=True)
	profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))
	publicationid = db.Column(db.Integer,db.ForeignKey('publications.id', onupdate='CASCADE', ondelete='CASCADE'))

class Publications(db.Model):
	__tablename__ = 'publications'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	author = db.Column(db.String(30))
	conference = db.Column(db.String(100))
	report_no = db.Column(db.String(100))
	abstract = db.Column(db.Text)
	date_published = db.Column(db.String(50))
	likes = db.Column(db.Integer)
	pdf = db.Column(db.Text)


class Labs(db.Model):
	__tablename__ = 'labs'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	url = db.Column(db.String(100))
	description = db.Column(db.Text)
	num_followers = db.Column(db.Integer)


class Students(db.Model):
	__tablename__ = 'students'

	rollno = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(50))
	name = db.Column(db.String(60))
	fname = db.Column(db.String(20))
	mname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	email = db.Column(EmailType)
	stream = db.Column(db.String(30))	
	yearofjoin = db.Column(db.Integer)


class Professors(db.Model):
	__tablename__ = 'professors'

	profid = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(50))
	name = db.Column(db.String(60))
	fname = db.Column(db.String(20))
	mname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	email = db.Column(EmailType)
	research_center = db.Column(db.String(30))	
	yearofjoin = db.Column(db.Integer)

class Student_following_Students(db.Model):
	__tablename__ = 'student_following_students'

	tempid = db.Column(db.Integer, primary_key=True)
	rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))
	followed_rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))


class Professor_following_Professors(db.Model):
	__tablename__ = 'professor_following_professors'

	tempid = db.Column(db.Integer, primary_key=True)
	profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))
	followed_profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))
	
class Student_following_Professors(db.Model):
	__tablename__ = 'student_following_professors'

	tempid = db.Column(db.Integer, primary_key=True)
	rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))
	profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))


class Student_following_Labs(db.Model):
	__tablename__ = 'student_following_labs'

	tempid = db.Column(db.Integer, primary_key=True)
	rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))
	labid = db.Column(db.Integer,db.ForeignKey('labs.id', onupdate='CASCADE', ondelete='CASCADE'))

class Professor_following_Students(db.Model):
	__tablename__ = 'professor_following_students'

	tempid = db.Column(db.Integer, primary_key=True)
	profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))
	rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))

class Professor_following_Labs(db.Model):
	__tablename__ = 'professor_following_labs'

	tempid = db.Column(db.Integer, primary_key=True)
	profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))
	labid = db.Column(db.Integer,db.ForeignKey('labs.id', onupdate='CASCADE', ondelete='CASCADE'))


class Professor_enrolledin_Labs(db.Model):
	__tablename__ = 'professor_enrolledin_labs'

	tempid = db.Column(db.Integer, primary_key=True)
	profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))
	labid = db.Column(db.Integer,db.ForeignKey('labs.id', onupdate='CASCADE', ondelete='CASCADE'))

class Student_enrolledin_Labs(db.Model):
	__tablename__ = 'student_enrolledin_labs'

	tempid = db.Column(db.Integer, primary_key=True)
	rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))
	labid = db.Column(db.Integer,db.ForeignKey('labs.id', onupdate='CASCADE', ondelete='CASCADE'))

class Student_owns_Publications(db.Model):
	__tablename__ = 'student_owns_publications'
	tempid = db.Column(db.Integer, primary_key=True)
	rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))
	publicationid = db.Column(db.Integer,db.ForeignKey('publications.id', onupdate='CASCADE', ondelete='CASCADE'))

class Professor_owns_Publications(db.Model):
	__tablename__ = 'professor_owns_publications'
	tempid = db.Column(db.Integer, primary_key=True)
	profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))
	publicationid = db.Column(db.Integer,db.ForeignKey('publications.id', onupdate='CASCADE', ondelete='CASCADE'))


class Num_following_Student(db.Model):
	__tablename__ = 'num_following_student'

	tempid = db.Column(db.Integer, primary_key=True)
	num = db.Column(db.Integer)
	followed_rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))


class Num_following_Professor(db.Model):
	__tablename__ = 'num_following_professor'

	tempid = db.Column(db.Integer, primary_key=True)
	num = db.Column(db.Integer)
	followed_profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))

class Num_following_Lab(db.Model):
	__tablename__ = 'num_following_lab'

	tempid = db.Column(db.Integer, primary_key=True)
	num = db.Column(db.Integer)
	followed_labid = db.Column(db.Integer,db.ForeignKey('labs.id', onupdate='CASCADE', ondelete='CASCADE'))

class Publication_in_fields(db.Model):
	__tablename__ = 'publication_in_fields'

	tempid = db.Column(db.Integer, primary_key=True)
	publicationid = db.Column(db.Integer,db.ForeignKey('publications.id', onupdate='CASCADE', ondelete='CASCADE'))
	field = db.Column(db.String(50))

class Professor_in_fields(db.Model):
	__tablename__ = 'professor_in_fields'

	tempid = db.Column(db.Integer, primary_key=True)
	profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))
	field = db.Column(db.String(50))

class Student_in_fields(db.Model):
	__tablename__ = 'student_in_fields'

	tempid = db.Column(db.Integer, primary_key=True)
	rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))
	field = db.Column(db.String(50))

class Student_under_Professor(db.Model):
	__tablename__ = 'student_under_professor'

	tempid = db.Column(db.Integer, primary_key=True)
	rollno = db.Column(db.Integer,db.ForeignKey('students.rollno', onupdate='CASCADE', ondelete='CASCADE'))
	profid = db.Column(db.Integer,db.ForeignKey('professors.profid', onupdate='CASCADE', ondelete='CASCADE'))


db.create_all()


all_research_fields = ['Natural Language Processing','Machine Learning','Machine Translation','Computer vision','Pattern recognition', 'Robotic Vision','System and network security','Cryptography','Biometrics','Speech Recognition']


def following(category, id):
	following_papers = []
	if category == "Professor":
		Following_prof_ids = Professor_following_Professors.query.filter_by(profid=id).all()
		Following_stud_ids = Professor_following_Students.query.filter_by(profid=id).all()

		for prof in Following_prof_ids:
			prof_papers_ids = Professor_owns_Publications.query.filter_by(profid=prof.followed_profid).order_by(Professor_owns_Publications.publicationid.desc()).limit(4).all()
			for paper in prof_papers_ids:
				following_papers.append(Publications.query.filter_by(id=paper.publicationid).first())
		
		for stud in Following_stud_ids:
			stud_papers_ids = Student_owns_Publications.query.filter_by(rollno=stud.rollno).order_by(Student_owns_Publications.publicationid.desc()).limit(4).all()
			for paper in stud_papers_ids:
				following_papers.append(Publications.query.filter_by(id=paper.publicationid).first())
	else:
		Following_prof_ids = Student_following_Professors.query.filter_by(rollno=id).all()
		Following_stud_ids = Student_following_Students.query.filter_by(rollno=id).all()

		for prof in Following_prof_ids:
			prof_papers_ids = Professor_owns_Publications.query.filter_by(profid=prof.profid).order_by(Professor_owns_Publications.publicationid.desc()).limit(4).all()
			for paper in prof_papers_ids:
				following_papers.append(Publications.query.filter_by(id=paper.publicationid).first())
		
		for stud in Following_stud_ids:
			stud_papers_ids = Student_owns_Publications.query.filter_by(rollno=stud.followed_rollno).order_by(Student_owns_Publications.publicationid.desc()).limit(4).all()
			for paper in stud_papers_ids:
				following_papers.append(Publications.query.filter_by(id=paper.publicationid).first())
	
	following_papers.sort(key=lambda r: r.date_published,reverse=True)
	# following_papers = sorted(following_papers, key=attrgetter('person.birthdate'))

	return following_papers

# class Professor(db.Model):
# 	id

# Index
@app.route('/')
@app.route('/index')
def index():
	if 'logged_in' in session:
		return redirect(url_for('home'))

	labs = Labs.query.order_by(Labs.id.asc()).all()
	papers = Publications.query.order_by(Publications.likes.desc()).all()
	num_lab = Num_following_Lab.query.all()
	return render_template('index.html',labs=labs, papers=papers,num_lab=num_lab)

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			# flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap


# Articles
@app.route('/articles')
def articles():
	papers = Publications.query.order_by(Publications.likes.desc()).all()
	# authors = Publications_authors.query.order_by(Publications_authors.id.desc()).all()

	my_research_fields = []

	if session['category'] == "Professor":
		pub_likes = Professor_likes_Publications.query.filter_by(profid=session['prof_id']).all()
		my_research_fields = Professor_in_fields.query.filter_by(profid=session['prof_id']).all()
	else:
		pub_likes = Student_likes_Publications.query.filter_by(rollno=session['rollno']).all()
		my_research_fields = Student_in_fields.query.filter_by(rollno=session['rollno']).all()

	research_fields = []
	for i in my_research_fields:
		research_fields.append(str(i.field))

	if len(papers) > 0:
		return render_template('articles.html', papers=papers,pub_likes=pub_likes, my_research_fields=research_fields, all_research_fields=all_research_fields)
	else:
		error = 'No Publications Found'
		return render_template('articles.html', error=error, my_research_fields=research_fields, all_research_fields=all_research_fields)


# route for labs page
@app.route('/labs')
@is_logged_in
def labs():
	lab = Labs.query.order_by(Labs.id.asc()).all()
	following_labs = None
	enrolled_labs = None
	my_research_fields = []
	if session['category'] == "Professor":
		following_labs = Professor_following_Labs.query.filter_by(profid=session['prof_id']).all()
		my_research_fields = Professor_in_fields.query.filter_by(profid=session['prof_id']).all()
	else:
		following_labs = Student_following_Labs.query.filter_by(rollno=session['rollno']).all()
		my_research_fields = Student_in_fields.query.filter_by(rollno=session['rollno']).all()

	research_fields = []
	for i in my_research_fields:
		research_fields.append(str(i.field))

	if session['category'] == "Professor":
		enrolled_labs = Professor_enrolledin_Labs.query.filter_by(profid=session['prof_id']).all()
	else:
		enrolled_labs = Student_enrolledin_Labs.query.filter_by(rollno=session['rollno']).all()

	num_lab = Num_following_Lab.query.all()
	print(following_labs)
	if len(lab) > 0:
		return render_template('labs.html', lab=lab,following_labs=following_labs,num_lab=num_lab, enrolled_labs=enrolled_labs, my_research_fields=research_fields, all_research_fields=all_research_fields)
	else:
		error = 'No Labs Found'
		return render_template('labs.html', error=error, my_research_fields=research_fields, all_research_fields=all_research_fields)


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
	# form = RegisterForm(request.form)
	if request.method == 'POST':
		# name = form.name.data
		email = request.form['email']
		# username = form.username.data
		category = request.form['category']

		print (str(request.form['password']))
		print (str(request.form['confirm_password']))

		# check entered passwords
		password = sha256_crypt.encrypt(request.form['password'])
		# password_candidate = request.form['password']
		confirm_password = request.form['confirm_password']

		user=None
		if category == "Professor":
			user = Professors.query.filter_by(email=email).first()
		else:
			user = Students.query.filter_by(email=email).first()

		if user is None:
			flash('Email Id doesn\'t exist!!', 'danger')
			return redirect(url_for('register'))

		if not sha256_crypt.verify(confirm_password, password):
			flash('Passwords do not match!!', 'danger')
			return redirect(url_for('register'))

		user.password = password
		db.session.commit()

		flash('You are now registered and can log in', 'success')
		return redirect(url_for('register'))

	return render_template('register.html')


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'logged_in' in session:
		return redirect(url_for('home'))

	if request.method == 'POST':
		# Get Form Fields
		emailid = request.form['emailid']
		password_candidate = request.form['password']
		category = request.form['category']

		prof=None
		student=None
		if category == "Professor":
			prof = Professors.query.filter_by(email=emailid).first()

			if prof is None:
				error = 'Entry not found'
				return render_template('login.html', error=error)

			password = prof.password
			name = prof.name
			fname = prof.fname
		else:
			student = Students.query.filter_by(email=emailid).first()

			if student is None:
				error = 'Entry not found'
				return render_template('login.html', error=error)

			password = student.password
			name = student.name
			fname = student.fname

		if prof is not None or student is not None:

			# Compare Passwords
			if sha256_crypt.verify(password_candidate, password):
				# Passed
				session['logged_in'] = True
				session['emailid'] = emailid
				if category == "Professor":
					session['prof_id'] = prof.profid
				else:
					session['rollno'] = student.rollno
				session['category'] = category
				session['name'] = name
				session['fname'] = fname
				session['profile_img'] = fname + ".jpg"

				return redirect(url_for('home'))
			else:
				error = 'Invalid login'
				return render_template('login.html', error=error)
		else:
			error = 'Entry not found'
			return render_template('login.html', error=error)

	return render_template('login.html')


# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('index'))


# Trending
@app.route('/trending')
@is_logged_in
def trending():
	students_data = []
	professors_data = []
	labs_data = []
	publications_data = []
	students = Num_following_Student.query.order_by(Num_following_Student.num.desc()).limit(5).all()
	professors = Num_following_Professor.query.order_by(Num_following_Professor.num.desc()).limit(5).all()
	labs = Num_following_Lab.query.order_by(Num_following_Lab.num.desc()).limit(5).all()
	publications = Publications.query.order_by(Publications.likes.desc()).limit(5).all()
	for i in students:
		students_data.append(Students.query.filter_by(rollno=i.followed_rollno).first())
	for j in professors:
		professors_data.append(Professors.query.filter_by(profid=j.followed_profid).first())
	for k in labs:
		labs_data.append(Labs.query.filter_by(id=k.followed_labid).first())
	for l in publications:
		publications_data.append(Publications.query.filter_by(id=l.id).first())

	my_research_fields = []
	if session['category'] == "Professor":
		my_research_fields = Professor_in_fields.query.filter_by(profid=session['prof_id']).all()
	else:
		my_research_fields = Student_in_fields.query.filter_by(rollno=session['rollno']).all()

	research_fields = []
	for i in my_research_fields:
		research_fields.append(str(i.field))

	return render_template('trending.html',students=students,students_data=students_data,professors=professors,professors_data=professors_data,labs = labs,labs_data = labs_data,publications=publications,publications_data=publications_data, my_research_fields=research_fields, all_research_fields=all_research_fields)



# Professor
@app.route('/professor')
@is_logged_in
def professor():
	return render_template('professor.html')


# Student
@app.route('/home')
@is_logged_in
def home():
	papers = Publications.query.order_by(Publications.id.asc()).all()
	my_papers = []
	my_labs = []
	my_research_fields = []
	following_papers=[]
	pub_likes=[]
	if session['category'] == "Professor":
		own_paper_ids = Professor_owns_Publications.query.filter_by(profid=session['prof_id']).all()
		for paper in own_paper_ids:
			my_papers.append(Publications.query.filter_by(id=paper.publicationid).first())
		
		own_labs_ids = Professor_enrolledin_Labs.query.filter_by(profid=session['prof_id']).all()
		for lab in own_labs_ids:
			my_labs.append(Labs.query.filter_by(id=lab.labid).first())

		my_research_fields = Professor_in_fields.query.filter_by(profid=session['prof_id']).all()
		following_papers=following("Professor", session['prof_id'])
		pub_likes = Professor_likes_Publications.query.filter_by(profid=session['prof_id']).all()
	else:
		own_paper_ids = Student_owns_Publications.query.filter_by(rollno=session['rollno']).all()
		for paper in own_paper_ids:
			my_papers.append(Publications.query.filter_by(id=paper.publicationid).first())

		own_labs_ids = Student_enrolledin_Labs.query.filter_by(rollno=session['rollno']).all()
		for lab in own_labs_ids:
			my_labs.append(Labs.query.filter_by(id=lab.labid).first())

		my_research_fields = Student_in_fields.query.filter_by(rollno=session['rollno']).all()
		following_papers=following("Student", session['rollno'])
		pub_likes = Student_likes_Publications.query.filter_by(rollno=session['rollno']).all()

	# print(my_research_fields)
	research_fields = []
	for i in my_research_fields:
		research_fields.append(str(i.field))

	profs = []
	studs = []
	labs = []
	num_labs = []
	num_profs = []
	num_studs = []
	if session['category'] == "Professor":
		follow_prof = Professor_following_Professors.query.filter_by(profid=session['prof_id']).all()
		follow_stud = Professor_following_Students.query.filter_by(profid=session['prof_id']).all()
		follow_lab = Professor_following_Labs.query.filter_by(profid=session['prof_id']).all()

		for i in follow_prof:
			profs.append(Professors.query.filter_by(profid=i.followed_profid).first())
		for i in follow_stud:
			studs.append(Students.query.filter_by(rollno=i.rollno).first())
		for i in follow_lab:
			labs.append(Labs.query.filter_by(id=i.labid).first())
	else:
		follow_prof = Student_following_Professors.query.filter_by(rollno=session['rollno']).all()
		follow_stud = Student_following_Students.query.filter_by(rollno=session['rollno']).all()
		follow_lab = Student_following_Labs.query.filter_by(rollno=session['rollno']).all()

		for i in follow_prof:
			profs.append(Professors.query.filter_by(profid=i.profid).first())
		for i in follow_stud:
			studs.append(Students.query.filter_by(rollno=i.followed_rollno).first())
		for i in follow_lab:
			labs.append(Labs.query.filter_by(id=i.labid).first())

	num_labs = Num_following_Lab.query.all()
	num_studs = Num_following_Student.query.all()
	num_profs = Num_following_Professor.query.all()
	
	following_labs = None
	if session['category'] == "Professor":
		following_labs = Professor_following_Labs.query.filter_by(profid=session['prof_id']).all()
	else:
		following_labs = Student_following_Labs.query.filter_by(rollno=session['rollno']).all()
	num_lab = Num_following_Lab.query.all()

	my_student = []
	if session['category'] == "Professor":
		my_student_id = Student_under_Professor.query.filter_by(profid=session['prof_id']).all()
		for i in my_student_id:
			my_student.append(Students.query.filter_by(rollno=i.rollno).first())
	else:
		my_student_id = Student_under_Professor.query.filter_by(rollno=session['rollno']).all()
		for i in my_student_id:
			my_student.append(Professors.query.filter_by(profid=i.profid).first())

	return render_template('home.html', papers=papers, my_papers=my_papers, my_labs=my_labs,following_papers=following_papers,pub_likes=pub_likes, following_labs=following_labs, num_lab=num_lab,profs=profs,studs=studs,labs=labs,num_labs=num_labs,num_profs=num_profs,num_studs=num_studs,my_student=my_student, my_research_fields=research_fields, all_research_fields=all_research_fields)


# Article Form Class
class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=200)])
	body = TextAreaField('Body', [validators.Length(min=30)])
	

# Add Publication
@app.route('/add_paper', methods=['GET', 'POST'])
@is_logged_in
def add_paper():
	if request.method == "POST":
		title = request.form['title']
		# author = request.form['author']
		author = session['name']
		conference = request.form['conference']
		date = request.form['date']
		report_no = request.form['report_no']
		pdf = request.form['pdf']
		editor = request.form['editor']
		research_fields = request.form.getlist('field_of_research')

		# Create new paper
		paper = Publications(title=title, author=author, conference=conference, date_published=date, report_no=report_no,likes=0, abstract=editor, pdf=pdf)
		db.session.add(paper)
		db.session.commit()

		# Add user to database
		if session['category'] == "Professor":
			prof_pub = Professor_owns_Publications(profid=session['prof_id'],publicationid=paper.id)
			db.session.add(prof_pub)
		else:
			stud_pub = Student_owns_Publications(rollno=session['rollno'],publicationid=paper.id)
			db.session.add(stud_pub)

		db.session.commit()

		for fld in research_fields:
			entry = Publication_in_fields(publicationid=paper.id, field=fld)
			db.session.add(entry)
			db.session.commit()

	return redirect(url_for('home'))


@app.route('/add_research_fields', methods=['GET', 'POST'])
@is_logged_in
def add_research_fields():
	if request.method == "POST":
		if session['category'] == "Professor":
			entries = Professor_in_fields.query.filter_by(profid = session['prof_id']).all()
			for e in entries:
				db.session.delete(e)
				db.session.commit()
		else:
			entries = Student_in_fields.query.filter_by(rollno = session['rollno']).all()
			for e in entries:
				db.session.delete(e)
				db.session.commit()

		research_fields = request.form.getlist('field_of_research')

		print (research_fields)
		entry = None
		for f in research_fields:
			if session['category'] == "Professor":
				entry = Professor_in_fields(profid=session['prof_id'], field=f)
			else:
				entry = Student_in_fields(rollno=session['rollno'], field=f)
			db.session.add(entry)
			db.session.commit()		

	return redirect(url_for('home'))


@app.route('/professor/<string:id>')
@is_logged_in
def search_prof(id):
	prof = Professors.query.filter_by(profid=id).first()
	papers = Publications.query.order_by(Publications.id.asc()).all()
	# authors = Publications_authors.query.order_by(Publications_authors.id.asc()).all()
	my_papers = []
	my_labs = []
	own_paper_ids = Professor_owns_Publications.query.filter_by(profid=id).all()
	for paper in own_paper_ids:
		my_papers.append(Publications.query.filter_by(id=paper.publicationid).first())
	
	own_labs_ids = Professor_enrolledin_Labs.query.filter_by(profid=id).all()
	for lab in own_labs_ids:
		my_labs.append(Labs.query.filter_by(id=lab.labid).first())

	print(my_labs)

	following_papers=following("Professor", id)
	pub_likes = Professor_likes_Publications.query.filter_by(profid=id).all()

	my_research_fields = []
	if session['category'] == "Professor":
		my_research_fields = Professor_in_fields.query.filter_by(profid=session['prof_id']).all()
	else:
		my_research_fields = Student_in_fields.query.filter_by(rollno=session['rollno']).all()

	research_fields = []
	for i in my_research_fields:
		research_fields.append(str(i.field))

	profs = []
	studs = []
	labs = []
	num_labs = []
	num_profs = []
	num_studs = []
	follow_prof = Professor_following_Professors.query.filter_by(profid=id).all()
	follow_stud = Professor_following_Students.query.filter_by(profid=id).all()
	follow_lab = Professor_following_Labs.query.filter_by(profid=id).all()

	for i in follow_prof:
		profs.append(Professors.query.filter_by(profid=i.followed_profid).first())
	for i in follow_stud:
		studs.append(Students.query.filter_by(rollno=i.rollno).first())
	for i in follow_lab:
		labs.append(Labs.query.filter_by(id=i.labid).first())

	num_labs = Num_following_Lab.query.all()
	num_studs = Num_following_Student.query.all()
	num_profs = Num_following_Professor.query.all()
	
	following_labs = None
	following_labs = Professor_following_Labs.query.filter_by(profid=id).all()

	num_lab = Num_following_Lab.query.all()

	my_student = []
	my_student_id = Student_under_Professor.query.filter_by(profid=id).all()
	for i in my_student_id:
		my_student.append(Students.query.filter_by(rollno=i.rollno).first())

	return render_template('professor.html', prof=prof, papers=papers, my_papers=my_papers, my_labs=my_labs,following_papers=following_papers,pub_likes=pub_likes, following_labs=following_labs, num_lab=num_lab,profs=profs,studs=studs,labs=labs,num_labs=num_labs,num_profs=num_profs,num_studs=num_studs,my_student=my_student,my_research_fields=research_fields, all_research_fields=all_research_fields)


@app.route('/student/<string:rollno>')
@is_logged_in
def search_stud(rollno):
	student = Students.query.filter_by(rollno=rollno).first()
	papers = Publications.query.order_by(Publications.id.asc()).all()
	# authors = Publications_authors.query.order_by(Publications_authors.id.asc()).all()
	my_papers = []
	my_labs = []
	own_paper_ids = Student_owns_Publications.query.filter_by(rollno=rollno).all()
	for paper in own_paper_ids:
		my_papers.append(Publications.query.filter_by(id=paper.publicationid).first())

	own_labs_ids = Student_enrolledin_Labs.query.filter_by(rollno=rollno).all()
	for lab in own_labs_ids:
		my_labs.append(Labs.query.filter_by(id=lab.labid).first())
	
	following_papers=following("Student", rollno)
	pub_likes = Student_likes_Publications.query.filter_by(rollno=rollno).all()

	my_research_fields = []
	if session['category'] == "Professor":
		my_research_fields = Professor_in_fields.query.filter_by(profid=session['prof_id']).all()
	else:
		my_research_fields = Student_in_fields.query.filter_by(rollno=session['rollno']).all()

	research_fields = []
	for i in my_research_fields:
		research_fields.append(str(i.field))

	profs = []
	studs = []
	labs = []
	num_labs = []
	num_profs = []
	num_studs = []

	follow_prof = Student_following_Professors.query.filter_by(rollno=rollno).all()
	follow_stud = Student_following_Students.query.filter_by(rollno=rollno).all()
	follow_lab = Student_following_Labs.query.filter_by(rollno=rollno).all()

	for i in follow_prof:
		profs.append(Professors.query.filter_by(profid=i.profid).first())
	for i in follow_stud:
		studs.append(Students.query.filter_by(rollno=i.followed_rollno).first())
	for i in follow_lab:
		labs.append(Labs.query.filter_by(id=i.labid).first())

	num_labs = Num_following_Lab.query.all()
	num_studs = Num_following_Student.query.all()
	num_profs = Num_following_Professor.query.all()
	
	following_labs = None
	following_labs = Student_following_Labs.query.filter_by(rollno=rollno).all()
	num_lab = Num_following_Lab.query.all()

	my_student = []
	my_student_id = Student_under_Professor.query.filter_by(rollno=rollno).all()
	for i in my_student_id:
		my_student.append(Professors.query.filter_by(profid=i.profid).first())
	# my_student = []
	# my_student_id = Student_under_Professor.query.filter_by(profid=id).all()
	# for i in my_student_id:
	# 	my_student.append(Students.query.filter_by(rollno=i.rollno).first())

	return render_template('student.html', student=student, papers=papers, my_student=my_student,my_papers=my_papers, my_labs=my_labs,following_papers=following_papers,pub_likes=pub_likes, following_labs=following_labs, num_lab=num_lab,profs=profs,studs=studs,labs=labs,num_labs=num_labs,num_profs=num_profs,num_studs=num_studs,my_research_fields=research_fields, all_research_fields=all_research_fields)



# Search
@app.route('/search', methods=['POST'])
def search():
	if request.method == 'POST':
		# Get Form Fields
		search_string = request.form['search_string']
		category = request.form['category']

		print (search_string)
		print (category)

		students = None
		professors = None
		prof_stud = None
		my_research_fields = []

		num_labs = Num_following_Lab.query.all()
		num_studs = Num_following_Student.query.all()
		num_profs = Num_following_Professor.query.all()
		if session['category'] == "Professor":
			prof_stud = Student_under_Professor.query.filter_by(profid=session['prof_id']).all()
			following_labs = Professor_following_Labs.query.filter_by(profid=session['prof_id']).all()
			following_prof = Professor_following_Professors.query.filter_by(profid=session['prof_id']).all()
			following_stud = Professor_following_Students.query.filter_by(profid=session['prof_id']).all()
			my_research_fields = Professor_in_fields.query.filter_by(profid=session['prof_id']).all()
		else:
			prof_stud = Student_under_Professor.query.filter_by(rollno=session['rollno']).all()
			following_labs = Student_following_Labs.query.filter_by(rollno=session['rollno']).all()
			following_prof = Student_following_Professors.query.filter_by(rollno=session['rollno']).all()
			following_stud = Student_following_Students.query.filter_by(rollno=session['rollno']).all()
			my_research_fields = Student_in_fields.query.filter_by(rollno=session['rollno']).all()

		research_fields = []
		for i in my_research_fields:
			research_fields.append(str(i.field))

		if category == "Student":
			students = Students.query.filter_by(name=search_string).all()
			return render_template('search.html', search_string=search_string, students=students,following_labs=following_labs,following_prof=following_prof,following_stud=following_stud, num_studs=num_studs,prof_stud=prof_stud, my_research_fields=research_fields, all_research_fields=all_research_fields)		
		elif category == "Professor":
			professors = Professors.query.filter_by(name=search_string).all()
			return render_template('search.html', search_string=search_string, professors=professors,following_labs=following_labs,following_prof=following_prof,following_stud=following_stud, num_profs=num_profs,prof_stud=prof_stud, my_research_fields=research_fields, all_research_fields=all_research_fields)
		elif category == "Lab":
			labs = Labs.query.filter_by(name=search_string).all()
			num_labs = []
			for lab in labs:
				l = Num_following_Lab.query.filter_by(followed_labid=lab.id).first()
				num_labs.append(l)
			return render_template('search.html', search_string=search_string, labs=labs, num_labs=num_labs,following_labs=following_labs,following_prof=following_prof,following_stud=following_stud, my_research_fields=research_fields, all_research_fields=all_research_fields)
		elif category == "Field of Interest":
			pub_ids = Publication_in_fields.query.filter_by(field=search_string)
			print (pub_ids)
			publications = []
			for pub in pub_ids:
				pubn = Publications.query.filter_by(id=pub.publicationid).first()
				publications.append(pubn)
			return render_template('search.html', search_string=search_string, publications=publications,following_labs=following_labs,following_prof=following_prof,following_stud=following_stud, my_research_fields=research_fields, all_research_fields=all_research_fields)


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
	# flash('Article Deleted', 'success')

	return redirect(url_for('dashboard'))

def add_dummy():
	lab = [
		{
			'lab_id': '1',
			'name': 'Kohli Center on Intelligent Systems (KCIS)',
			'url': 'http://kcis.iiit.ac.in',
			'info': '<p><strong>Kohli Center on Intelligent Systems</strong> (KCIS) was established at <strong>International Institute of Information Technology, Hyderabad</strong> (IIIT Hyderabad) in 2015 with funding from <strong>Tata Consultancy Services</strong> (TCS) to give a fillip to research, teaching and entrepreneurship in the broad Intelligent Systems area.</p>'
		},
		{
			'lab_id': '2',
			'name': 'Signal Processing and Communications Research Center (SPCRC)',
			'url': 'http://spcrc.iiit.ac.in/',
			'info': '<p>SPCRC was set up in 2003 with the goal of undertaking fundamental research in signal processing and communication engineering. Research, at theoretical and applied levels, is conducted in this center. Funding sources have included MCIT, DST, GE Global Research, Bangalore etc.</p>'
		},
		{
			'lab_id': '3',
			'name': 'Data Sciences and Analytics Center (DSAC)',
			'url': 'http://dsac.iiit.ac.in/',
			'info': '<p>Data Sciences and Analytics Center conducts research, facilitates technology transfer, and builds systems in the broad area of data engineering. The center inculcates the culture of research in students by involving them in activities such as:</p>'


		},
		{
			'lab_id': '4',
			'name': 'Language Technologies Research Center (LTRC)',
			'url': 'http://ltrc.iiit.ac.in/',
			'info': '<p>The LTRC addresses the complex problem of understanding and processing natural languages in both speech and text modes.</p><ul><li>LTRC conducts research on both basic and applied aspects of language technology.</li><li>It is the largest academic centre of speech and language technology in India.</li><li>LTRC carries out its work through four labs, which work in synergy with each other.</li></ul><p>LTRC is also a lead participant in nation-wide mission-mode consortia projects to develop deployable technology in the areas of Indian Language Machine Translation, English to Indian Language Machine Translation, and Cross Language Information Access (search engines).</p><h4>NLP-MT Lab</h4><p>The NLP-MT lab does fundamental work on developing grammatical as well statistical modelling of languages. Linguistic approaches are combined with machine learning techniques leading to new theories and technology development. This has resulted in higher accuracy parts-of-speech taggers, chunkers, constraint-based parsers as well as broad coverage statistical parsers, and semantic analyzers for Indian languages on the one hand, and annotated data including dependency tree banks, discourse banks, parallel corpora, etc. on the other.</p><h4>Anusaaraka Lab</h4><p>Anusaaraka lab is concerned with the development of machine translation systems which in addition to the usual machine translation output also allows a user to understand the source language text in a pseudo target language. For example, a reader who knows Hindi (target language) would be able to read the English source text, in a pseudo Hindi output after a small amount of training.</p>'
		},
		{
			'lab_id': '5',
			'name': 'Robotics Research Center (RRC)',
			'url': 'http://robotics.iiit.ac.in/',
			'info': '<p>The IIIT-H Robotics Research Lab works on research problems and innovative projects that extend the state-of-the-art in robotics. The center has worked in multiple domains of robotics involving Multi-robotic systems, Mobile robot navigation and planning, Mechanism design of All Terrain Vehicles and Robot Vision. The lab is well equipped with robot platforms and advanced sensors and has been publishing in top international conferences like ICRA, IROS, ICCV, AAMAS. The center is being and has been funded by various organizations both private, public and government. These include BARC, CAIR, Renault-Nissan, CVRDE, DRDO, DST, DIT and by IIIT Seed Grants The Robotics Research Center also collaborates with well known organizations and research labs such as CAIR, Bengaluru and BARC, Mumbai.</p><p><strong>Resources and Infrastructure:</strong> The lab is equipped with various robot test beds that are used in the research. These include ground robots like the pioneer P3-DX, the all terrain P3-AT along with the aerial robots like the parrot and the pelican. Along with these robots it is also equipped with a wide range of cameras and sensors.</p><p><strong>Mobile Robotics: </strong>Localization, mapping and navigation of robots in indoors and outdoor environments.</p><p><strong>Robot Mechanisms:</strong> Mechanical design and analysis of all-terrain vehicles.</p><p><strong>Multi Robots:</strong> Exploration and localization using multiple robots.</p><p><strong>Robotic Vision: </strong>Vision Processing algorithms for localization, mapping and classification.</p><h4>Current Research Areas</h4><div><p><strong>Robotic Vision</strong></p><ul><li>Independent Motion Detection and Segmentation</li><li>Monocular SLAM in Dynamic Environments</li><li>Monocular Localization</li><li>Structure Aided Visual SLAM</li><li>Visual Servoing for Space Robots</li></ul><p><strong>Multi Robotic Systems</strong></p><ul><li>Ground-Aerial Vehicle Coordination</li><li>Multi Robotic Exploration</li><li>Multi Robotic Collision Avoidance</li></ul><p><strong>Mobile and Embedded Robotics</strong></p><ul><li>Semantically Navigated Wheel Chair Systems</li><li>Object Search and Localization</li><li>FPGA Architectures for Mobile Robots</li></ul><p><strong>Mechanism Design</strong></p><ul><li>Active and Passive Mechanisms for All Terrain Navigation</li><li>Quadruped and Biped Design and Fabrication</li><li>Gait Generation for Quadruped and Wheeled Legged Systems</li></ul></div><h4>Faculty</h4><ul><li>Madhava Krishna K.</li><li>Rambabu Kalla</li><li>Suril Vijaykumar Shah</li></ul>'
		},
		{
			'lab_id': '6',
			'name': 'Center for Security, Theory and Algorithms (CSTAR)',
			'url': 'http://web2py.iiit.ac.in/research_centres/default/view_area/6',
			'info': '<p>The goal of the center is to do research in information security, theory and algorithms. It also participates in teaching various programmes of the Institute by offering various mandatory and elective courses in the areas of theoretical computer science and information security.</p><p>The center runs an M.Tech in CSIS (Computer Science &amp; Information Security) with support from MCIT Government of India (Ministry of Communications &amp; Information Technology) and participates in programmes of the Institute such as PhD / MS / Dual degree etc. with a specialization in algorithms, theoretical computer Science or information security. The center aspires to be</p><ul><li>A resource center for conceptualizing through fundamental insights</li><li>A knowledge center for effectively imparting the state-of-the-art in Theoretical computer Science and in Information Security</li><li>An accessible medium for disseminating and sharing expertise towards scientific and societal impact</li></ul><h4>Current Research Areas</h4><ul><li>System and network security</li><li>Security issues in wireless sensor networks</li><li>Multicore and manycore computing</li><li>Quantam information theory</li><li>Quantam information processing</li><li>Distributed graph algorithms</li><li>Cryptography</li><li>Geometric algorithms and data structures for large scale VLSI layouts</li></ul><h4>Faculty</h4><ul><li>Ashok Kumar Das</li><li>Bezawada Bruhadeshwar</li><li>Indranil Chakrabarty</li><li>Kannan Srinathan</li><li>Kishore Kothapalli</li><li>Shatrunjay Rawat</li></ul>'
		},
		{
			'lab_id': '7',
			'name': 'Software Engineering Research Center (SERC)',
			'url': 'https://serc.iiit.ac.in/',
			'info': '<p>Software engineering is the engineering of large and complex software systems. It focuses on systematic, disciplined, quantifiable approach to the development, operation, and maintenance of quality software, and the study of these approaches. SERC aims to lead the software engineering research in India by addressing India-specific issues in an industry-driven environment.</p><p>The main objectives of SERC are to focus on software engineering research, research in software engineering issues in the context of Indian software industry, operate closely with the industry by establishing touch points and to be a center of excellence driven by the industry for the industry.</p><p>Some of the major funded projects are state variable approach to the model-driven development of software for reactive systems (funded by SIEMENS), virtual Labs Integration (funded by MHRD), standardization of mobile interfaces (funded by CA Technologies) and big data analytics on the cloud (funded by CA Technologies).</p><h4>Current Research Areas</h4><ul><li>Software architectures and software reuse</li><li>Software engineering education</li><li>Programming languages</li><li>Mathematical computer science and formal methods</li><li>Technology for education</li><li>Model driven development</li><li>Process engineering</li><li>Semantic web architectures</li><li>Human computer interaction</li></ul><h4>Faculty</h4><ul><li>Kesav V. Nori</li><li>Raghu Reddy Y.</li><li>Ramesh Loganathan</li><li>Vasudeva Varma</li><li>Venkatesh Choppella</li><li>Viswanath K.</li><li>Suresh Purini</li></ul>'
		},
		{
			'lab_id': '8',
			'name': 'Center for Visual Information Technology (CVIT)',
			'url': 'http://cvit.iiit.ac.in/',
			'info': '<p>CVIT focuses on basic and advanced research in image processing, computer vision, computer graphics and machine learning. This center deals with the generation, processing, and understanding of primarily visual data as well as with the techniques and tools required doing so efficiently. The activity of this center overlaps the traditional areas of Computer Vision, Image Processing, Computer Graphics, Pattern Recognition and Machine Learning. CVIT works on both theoretical as well as practical aspects of visual information processing. Center aims to keep the right balance between the cutting edge academic research and impactful applied research.</p><p>Research projects are funded by various agencies like- Department of Science and Technology (DST), Naval Research Board (NRB), Ministry of Communications and Information Technology (MCIT), Defence Research and Development Organisation (DRDO), General Electric (GE), Nvidia and many more.</p><p>CVIT has around 50 students carrying out research for M.S. and Ph.D. degrees.</p><p>The center has regular visits and talks by leading researchers in the world.</p><h4>Current Research Areas</h4><ul><li>Document image processing especially recognition and retrieval</li><li>Biomedical and retinal image processing to aid doctors in diagnosis</li><li>Biometrics based on palm prints, handwriting, and hand geometry</li><li>Content-based annotation and search of large collections of images and videos</li><li>Machine learning for computer vision</li><li>Real-time rendering and streaming of large geometry including terrains and developing general purpose applications on the graphics processor units (GPUs) including graph algorithms, computer vision, and pattern recognition</li></ul><h4>Faculty</h4><ul><li>Anoop Namboodiri</li><li>Jawahar C. V.</li><li>Jayanthi Sivaswamy</li><li>Narayanan P. J.</li><li>Vineet Gandhi</li><li>Avinash Sharma</li></ul>'
		},
		{
			'lab_id': '9',
			'name': 'Center for VLSI and Embedded Systems Technology (CVEST)',
			'url': 'http://web2py.iiit.ac.in/research_centres/default/view_area/9',
			'info': '<p>The Center works in close collaboration with organizations such as Xilinx, Altera, Intel Corporation, DRDO etc. The center has three labs under its supervision - VLSI CAD Lab comprising of state-of-the-art VLSI CAD tools like CADENCE tools suite - Embedded Systems Lab-1 equipped with ARM Processor kits, ATMEGA8 and ATMEGA32 boards - Embedded Systems Lab-2 equipped with Altera FPGA Boards, TI Mixed Signal System Development kit, Intel Atom Processor boards. The facilities are available for all Institute staff and students who would like to participate in VLSI R&amp;D activity.</p><h4>Current Research Areas</h4><ul><li>Low power VLSI design</li><li>VLSI architectures</li><li>Biomedical embedded systems</li><li>Analog and mixed signal design</li><li>High speed communications in VLSI circuits</li><li>Multicore (Processor) architecture for embedded systems</li><li>ME, MS and MEM TRONICS</li><li>FPGA based embedded systems</li></ul><h4>Faculty</h4><ul><ul><li>Govindarajulu R.</li><li>Shubhajit Roy Chowdhury</li><li>Suresh Purini</li><li>Syed Azeemuddin</li></ul></ul><ul><li>Vijaya Sankara Rao P.</li></ul>'
		},
		{
			'lab_id': '10',
			'name': 'Computer Systems Group(CSG)',
			'url': 'http://csg.iiit.ac.in/',
			'info': '<p>The Computer Systems Group (CSG) was set-up in June 2017. Computer Systems Group undertakes research and development in all fundamental aspects of Computing Systems spanning across hardware and software. This group is actively involved in research and imparting advanced training through workshops, seminars, and semester long courses in the fields of computer architecture, compilers, computer networks, operating systems and other related topics. As a new group CSG today has about 3 faculty members and about 15 research students including Phd, Masters and honors students working on research topics that directly contribute and make an impact on the next-generation computing hardware and software.</p><h4>Current Research Areas</h4><ul><li>Computer Architecture</li><li>Compilers</li><li>Programming Languages</li><li>Computer Networks</li><li>Parallel and Distributed Computing</li><li>Cloud Computing</li><li>Systems Security</li><li>Internet of Things</li></ul><h4>Faculty</h4><ul><li>Suresh Purini</li><li>Venkatesh Choppella</li><li>Lavanya Ramapantulu</li></ul>'
		}
	]
	for data in lab:
		labs = Labs(name=data['name'],url=data['url'], description=data['info'], num_followers=0)
		db.session.add(labs)
	db.session.commit()

def add_num_lab():
	for i in range(10):
		lab_count = Num_following_Lab(num = 0,followed_labid = i+1)
		db.session.add(lab_count)
	db.session.commit()

@app.route('/follow_lab/<id>')
@is_logged_in
def follow_lab(id):
	lab = Num_following_Lab.query.filter_by(followed_labid=id).first()
	lab.num += 1
	print(lab.num)
	db.session.commit()

	if session['category'] == "Professor":
		prof = Professor_following_Labs(profid = session['prof_id'], labid = id)
		db.session.add(prof)
		db.session.commit()
	else:
		stud = Student_following_Labs(rollno = session['rollno'], labid = id)
		db.session.add(stud)
		db.session.commit()
	return str(lab.num)

@app.route('/unfollow_lab/<id>')
@is_logged_in
def unfollow_lab(id):
	lab = Num_following_Lab.query.filter_by(followed_labid=id).first()
	lab.num -= 1
	print(lab.num)
	db.session.commit()

	if session['category'] == "Professor":
		prof = Professor_following_Labs.query.filter_by(profid = session['prof_id']).filter_by(labid = id).first()
		db.session.delete(prof)
		db.session.commit()
	else:
		stud = Student_following_Labs.query.filter_by(rollno = session['rollno']).filter_by(labid = id).first()	
		db.session.delete(stud)
		db.session.commit()
	return str(lab.num)


@app.route('/follow_student/<id>')
@is_logged_in
def follow_student(id):
	stud = Num_following_Student.query.filter_by(followed_rollno=id).first()
	print(stud)
	if stud == None:
		stud = Num_following_Student(num = 1, followed_rollno = id)
		db.session.add(stud)
	else:	
		stud.num += 1
	db.session.commit()

	if session['category'] == "Professor":
		prof1 = Professor_following_Students(profid = session['prof_id'], rollno = id)
		db.session.add(prof1)
		db.session.commit()
	else:
		stud1 = Student_following_Students(rollno = session['rollno'], followed_rollno = id)
		db.session.add(stud1)
		db.session.commit()
	return str(stud.num)


@app.route('/unfollow_student/<id>')
@is_logged_in
def unfollow_student(id):
	stud = Num_following_Student.query.filter_by(followed_rollno=id).first()	
	stud.num -= 1
	db.session.commit()

	if session['category'] == "Professor":
		prof1 = Professor_following_Students.query.filter_by(profid = session['prof_id']).filter_by(rollno = id).first()
		db.session.delete(prof1)
		db.session.commit()
	else:
		stud1 = Student_following_Students.query.filter_by(rollno = session['rollno']).filter_by(followed_rollno = id).first()
		db.session.delete(stud1)
		db.session.commit()
	return str(stud.num)

@app.route('/follow_professor/<id>')
@is_logged_in
def follow_professor(id):
	prof = Num_following_Professor.query.filter_by(followed_profid=id).first()
	print(prof)
	if prof == None:
		prof = Num_following_Professor(num = 1, followed_profid = id)
		db.session.add(prof)
	else:	
		prof.num += 1
	db.session.commit()

	if session['category'] == "Professor":
		prof1 = Professor_following_Professors(profid = session['prof_id'], followed_profid = id)
		db.session.add(prof1)
		db.session.commit()
	else:
		prof1 = Student_following_Professors(rollno = session['rollno'], profid = id)
		db.session.add(prof1)
		db.session.commit()
	return str(prof.num)


@app.route('/unfollow_professor/<id>')
@is_logged_in
def unfollow_professor(id):
	prof = Num_following_Professor.query.filter_by(followed_profid=id).first()	
	prof.num -= 1
	db.session.commit()

	if session['category'] == "Professor":
		prof1 = Professor_following_Professors.query.filter_by(profid = session['prof_id']).filter_by(followed_profid = id).first()
		db.session.delete(prof1)
		db.session.commit()
	else:
		prof1 = Student_following_Professors.query.filter_by(rollno = session['rollno']).filter_by(profid = id).first()
		db.session.delete(prof1)
		db.session.commit()
	return str(prof.num)

@app.route('/like_pub/<id>')
@is_logged_in
def like_pub(id):
	pub = Publications.query.filter_by(id=id).first()	
	pub.likes += 1
	db.session.commit()

	if session['category'] == "Professor":
		prof = Professor_likes_Publications(profid = session['prof_id'], publicationid = id)
		db.session.add(prof)
		db.session.commit()
	else:
		stud = Student_likes_Publications(rollno = session['rollno'], publicationid = id)
		db.session.add(stud)
		db.session.commit()
	return str(pub.likes)

@app.route('/unlike_pub/<id>')
@is_logged_in
def unlike_pub(id):
	pub = Publications.query.filter_by(id=id).first()	
	pub.likes -= 1
	db.session.commit()

	if session['category'] == "Professor":
		prof = Professor_likes_Publications.query.filter_by(profid = session['prof_id']).filter_by(publicationid = id).first()
		db.session.delete(prof)
		db.session.commit()
	else:
		stud = Student_likes_Publications.query.filter_by(rollno = session['rollno']).filter_by(publicationid = id).first()
		db.session.delete(stud)
		db.session.commit()
	return str(pub.likes)

@app.route('/add_lab/<id>')
@is_logged_in
def add_lab(id):
	if session['category'] == "Professor":
		prof = Professor_enrolledin_Labs(profid=session['prof_id'], labid = id)
		db.session.add(prof)
	else:	
		stud = Student_enrolledin_Labs(rollno=session['rollno'], labid = id)
		db.session.add(stud)
	db.session.commit()
	return "lab added"

@app.route('/remove_lab/<id>')
@is_logged_in
def remove_lab(id):
	if session['category'] == "Professor":
		prof = Professor_enrolledin_Labs(profid=session['prof_id'], labid = id)
		db.session.delete(prof)
	else:	
		stud = Student_enrolledin_Labs(rollno=session['rollno'], labid = id)
		db.session.delete(stud)
	db.session.commit()
	return "lab removed"

@app.route('/add_professor/<id>')
@is_logged_in
def add_professor(id):
	stud_prof = Student_under_Professor.query.filter_by(profid=id).filter_by(rollno=session['rollno']).first()
	if stud_prof == None:
		stud_prof = Student_under_Professor(profid=id, rollno=session['rollno'])
		db.session.add(stud_prof)
		db.session.commit()
	return ""

@app.route('/remove_professor/<id>')
@is_logged_in
def remove_professor(id):
	stud_prof = Student_under_Professor.query.filter_by(rollno=session['rollno']).filter_by(profid = id).first()
	db.session.delete(stud_prof)
	db.session.commit()
	return ""

@app.route('/add_student/<id>')
@is_logged_in
def add_student(id):
	stud_prof = Student_under_Professor.query.filter_by(rollno=id).filter_by(profid=session['prof_id']).first()
	if stud_prof == None:
		stud_prof = Student_under_Professor(rollno=id, profid=session['prof_id'])
		db.session.add(stud_prof)
		db.session.commit()
	return ""

@app.route('/remove_student/<id>')
@is_logged_in
def remove_student(id):
	stud_prof = Student_under_Professor.query.filter_by(rollno=id).filter_by(profid =session['prof_id']).first()
	db.session.delete(stud_prof)
	db.session.commit()
	return ""