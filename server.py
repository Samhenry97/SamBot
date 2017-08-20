import os
import bcrypt, flask_login
import bots.sms, bots.kik, glob, database, reply, util
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask, render_template, flash, send_from_directory, abort, request, redirect, url_for, jsonify
from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(Form):
	firstName = StringField('First Name', [DataRequired(), Length(min=3, max=45)])
	lastName = StringField('Last Name', [DataRequired(), Length(min=3, max=45)])
	userName = StringField('Username', [DataRequired(), Length(min=3, max=45)])
	email = StringField('Email Address', [DataRequired(), Length(min=6, max=45)])
	password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Confirm Password')
	
class LoginForm(Form):
	email = StringField('Email Address or Username', [DataRequired()])
	password = PasswordField('Password', [DataRequired()])
	remember = BooleanField('Remember Me')
	
class UserForm(Form):
	firstName = StringField('First Name', [Length(max=45)])
	lastName = StringField('Last Name', [Length(max=45)])
	userName = StringField('Username', [Length(max=45)])
	nickName = StringField('Nickname', [Length(max=45)])
	phone = StringField('Phone Number', [Length(max=20)])
	email = StringField('Email Address')
	waitingFor = StringField('Waiting For')
	admin = BooleanField('Admin?')
	
class User(flask_login.UserMixin):
	def __init__(self, id, firstName, lastName, userName, nickName, waitingFor, email, password, admin, userId, type):
		self.id = id
		self.firstName = firstName
		self.lastName = lastName
		self.userName = userName
		self.nickName = nickName
		self.email = email
		self.waitingFor = waitingFor
		self.password = password
		self.admin = admin
		self.userId = userId
		self.type = type
		
	def update(self, firstName, lastName, userName, nickName, waitingFor, email, admin, userId):
		glob.db.update('UPDATE users SET firstName = %s, lastName = %s, userName = %s, waitingFor = %s, nickName = %s, email = %s, admin = %s, userId = %s WHERE id = %s',
			(firstName, lastName, userName, waitingFor, nickName, email, admin, userId, self.id))
		self.firstName = firstName
		self.lastName = lastName
		self.userName = userName
		self.waitingFor = waitingFor
		self.nickName = nickName
		self.email = email
		self.admin = admin
		self.userId = userId
		
	def delete(self):
		glob.db.deleteUser(self.id)
	
	def get(id):
		info = glob.db.getUserById(id)
		if info:
			return User(**info) if info else None
		
	def getByEmailOrUserName(email):
		info = glob.db.getUserByEmailOrUserName(email)
		if info:
			return User(**info) if info else None
			
	def all():
		return glob.db.selectMany('SELECT * FROM users;')

server = Flask(__name__)
loginManager = flask_login.LoginManager()

@loginManager.user_loader
def loadUser(userId):
	return User.get(int(userId))
	
@loginManager.unauthorized_handler
def unauthorized():
	flash('You must be logged in to view that page.', 'error')
	return redirect(url_for('register'))
	
def adminOnly():
	flash('You are unauthorized to view that page.', 'error')
	return redirect(url_for('index'))

@server.route('/sms', methods=['GET', 'POST'])
def smsMessage():
	return bots.sms.onMessage()

@server.route('/voice', methods=['GET', 'POST'])
def smsCall():
	return bots.sms.onVoice()
	
@server.route('/kik', methods=['GET', 'POST'])
def kikMessage():
	return bots.kik.onMessage()
	 
@server.route('/')
def index():
	return render_template('index.html', page='index')
	
@server.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		flash('You are already logged in.')
		return redirect(url_for('index'))
	
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		if glob.db.getUserByUserName(form.userName.data):
			flash('Username already taken.', 'error')
			return render_template('register.html', form=form)
		elif glob.db.getUserByEmail(form.email.data):
			flash('Looks like you\'ve already registered!')
			return render_template('register.html', form=form)
		hashed = bcrypt.hashpw(form.password.data, bcrypt.gensalt())
		glob.db.addUser(-1, form.firstName.data, form.lastName.data, form.userName.data, 'o', form.email.data, hashed)
		user = User.getByEmailOrUserName(form.email.data)
		login_user(user)
		flash('Thanks for signing up!')
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@server.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		flash('You are already logged in.')
		return redirect(url_for('index'))
		
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User.getByEmailOrUserName(form.email.data)
		if user and bcrypt.checkpw(form.password.data, user.password):
			login_user(user, remember=form.remember.data)
			flash('You\'ve successfully logged in!')
			return redirect(url_for('index'))
		flash('Incorrect email or password.', 'error')
	return render_template('login.html', form=form)
	
@server.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	form = UserForm(request.form)
	if request.method == 'POST' and form.validate():
		if current_user.userName != form.userName.data and glob.db.getUserByUserName(form.userName.data):
			flash('Username already taken.', 'error')
			return render_template('profile.html', form=form)
		if current_user.email != form.email.data and glob.db.getUserByEmail(form.email.data):
			flash('Email already taken.', 'error')
			return render_template('profile.html', form=form)
		try:
			form.admin.data = current_user.admin
			current_user.update(form.firstName.data, form.lastName.data, form.userName.data, form.nickName.data, form.waitingFor.data, form.email.data, form.admin.data, form.phone.data)
		except Exception as e:
			flash(str(e), 'error')
			return render_template('profile.html', form=form)
		flash('Profile saved!')
		return render_template('profile.html', form=form)
	form.firstName.data = current_user.firstName
	form.lastName.data = current_user.lastName
	form.userName.data = current_user.userName
	form.nickName.data = current_user.nickName
	form.phone.data = current_user.userId if current_user.userId != -1 else 0
	form.email.data = current_user.email
	form.waitingFor.data = current_user.waitingFor
	form.admin.data = current_user.admin
	return render_template('profile.html', form=form)
	
@server.route('/clearmessages')
@login_required
def clearMessages():
	glob.db.deleteUserMessages(current_user.id)
	flash('Your chat history has been cleared.')
	return redirect(url_for('profile'))
	
@server.route('/chat')
@login_required
def chat():
	messages = glob.db.getMessagesForUser(current_user.id)
	return render_template('chat.html', messages=messages, page='chat')
	
@server.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
	offset = int(request.args['offset']) if request.args.get('offset') else 0
	return jsonify(glob.db.getMessagesForUser(current_user.id, offset))
	
@server.route('/message', methods=['POST'])
@login_required
def message():
	text = request.get_json()['text']
	userInfo = glob.db.getUserById(current_user.id)
	chat = { 'id': -1, 'chatId': -1, 'chatUUID': '' }
	response = reply.getReply(text, userInfo, chat)
	glob.db.addMessage(userInfo['id'], text, True)
	glob.db.addMessage(userInfo['id'], response, False)
	return jsonify({'response': response})
	
@server.route('/reminders', methods=['POST'])
@login_required
def reminders():
	alerts = glob.db.getAlertsForUser(current_user.id)
	response = []
	for alert in alerts:
		if alert['time'] < util.getDate():
			if not alert['message']:
				message = 'Alarm!'
			else:
				message = 'Reminder: ' + alert['message']
			glob.db.addMessage(current_user.id, message, False)
			glob.db.deleteAlarm(alert['id'])
			response.append(message)
	return jsonify({'response': response})
			
	
@server.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have successfully logged out.')
	return redirect(url_for('index'))
	
@server.route('/about')
def about():
	return render_template('about.html', page='about')
	
@server.route('/users')
@login_required
def users():
	if not current_user.admin:
		return adminOnly()
	return render_template('users/index.html', users=User.all(), page='users')
	
@server.route('/users/<int:id>', methods=['GET', 'POST'])
@login_required
def editUser(id):
	if not current_user.admin:
		return adminOnly()
	form = UserForm(request.form)
	user = User.get(id)
	if not user:
		abort(404)
	if user.userName != form.userName.data and glob.db.getUserByUserName(form.userName.data):
		flash('Username already taken.', 'error')
		return render_template('users/edit.html', form=form, user=user)
	if user.email != form.email.data and glob.db.getUserByEmail(form.email.data):
		flash('Email already taken.', 'error')
		return render_template('users/edit.html', form=form, user=user)
	if request.method == 'POST' and form.validate():
		try:
			user.update(form.firstName.data, form.lastName.data, form.userName.data, form.nickName.data, form.waitingFor.data, form.email.data, form.admin.data, form.phone.data)
		except Exception as e:
			flash(str(e), 'error')
			return render_template('users/edit.html', form=form, user=user)
		flash('User saved!')
		return redirect(url_for('users'))
	form.firstName.data = user.firstName
	form.lastName.data = user.lastName
	form.userName.data = user.userName
	form.nickName.data = user.nickName
	form.email.data = user.email
	form.waitingFor.data = user.waitingFor
	form.admin.data = user.admin
	form.phone.data = user.userId if user.userId != -1 else 0
	return render_template('users/edit.html', form=form, user=user)
	
@server.route('/users/<int:id>/delete')
@login_required
def deleteUser(id):
	if not current_user.admin:
		return adminOnly()
	user = User.get(id)
	if not user:
		abort(404)
	user.delete()
	flash('User deleted.')
	return redirect(url_for('users'))
	
@server.route('/image/<path:fname>')
def image(fname):
	return send_from_directory('./res', fname)

@server.route('/favicon.ico')
def favicon():
	return send_from_directory('./res', 'favicon.ico', mimetype='image/vnd.microsoft.icon')
	
@server.errorhandler(404)
def notFound(e):
	return render_template('errors/404.html'), 404
	
@server.errorhandler(500)
def serverError(e):
	return render_template('errors/500.html'), 500
	
@server.after_request
def nocache(r):
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r

def listen(debug):
	loginManager.init_app(server)
	server.config.update(
		SECRET_KEY=os.environ['FLASK_SECRET'],
		SESSION_TYPE='filesystem',
		TEMPLATES_AUTO_RELOAD=debug,
		DEBUG=debug
	)
	server.run(port=8080)

if __name__ == '__main__':
	glob.db = database.Database()
	print('Listening...')
	listen(True)
