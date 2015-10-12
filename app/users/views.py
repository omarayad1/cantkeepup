from flask import Blueprint, redirect, render_template, request, url_for, \
		flash # pragma: no cover
from forms import LoginForm, RegisterForm # pragma: no cover
from app.models import User # pragma: no cover
from app import bcrypt, db # pragma: no cover
from flask.ext.login import login_user, login_required, logout_user \
		 # pragma: no cover

################
#### config ####
################

users_blueprint = Blueprint(
	'users', __name__,
	template_folder='templates'
) # pragma: no cover

################
#### routes ####
################

@users_blueprint.route('/login', methods=['GET', 'POST']) # pragma: no cover
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			user = User.query.filter_by( \
					username=request.form['username']).first()
			if user is not None and bcrypt.check_password_hash(user.password, \
					request.form['password']):
				login_user(user)
				flash('You were logged in.')
				return redirect(url_for('dashboard.dashboard'))
			else:
				error = 'Invalid Credentials. Please try again.'
	return render_template('login.html',form=form, error=error)

@users_blueprint.route('/logout') # pragma: no cover
@login_required # pragma: no cover
def logout():
	logout_user()
	flash('You were logged out.')
	return redirect(url_for('home.home'))

@users_blueprint.route('/register', methods=['GET', 'POST']) \
		# pragma: no cover
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(
			username=form.username.data,
			firstname=form.firstname.data,
			lastname=form.lastname.data,
			email=form.email.data,
			password=form.password.data
		)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		flash('Welcome '+user.firstname+' '+user.lastname+' to cantkeeup app')
		return redirect(url_for('home.home'))
	return render_template('register.html', form=form)
