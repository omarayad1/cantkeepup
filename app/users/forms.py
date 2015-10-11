from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User

class LoginForm(Form):
	username = TextField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(Form):

	firstname = TextField(
		'username',
		validators=[
			DataRequired(),
			Length(min=3, max=25)
		]
	)
	lastname = TextField(
		'username',
		validators=[DataRequired(), Length(min=3, max=25)]
	)
	username = TextField(
		'username',
		validators=[DataRequired(), Length(min=3, max=25)]
	)
	email = TextField(
		'email',
		validators=[DataRequired(), Email(message=None), Length(max=255)]
	)
	password = PasswordField(
		'password',
		validators=[DataRequired(), Length(min=6,max=50)]
	)
	confirm = PasswordField(
		'Repeat password',
		validators = [
			DataRequired(), EqualTo('password', message='Passwords must match.')
		]
	)

	def validate(self):
		rv = Form.validate(self)
		result = True
		if not rv:
			result = False

		user = User.query.filter_by(username=self.username.data).first()

		if user is not None:
			self.username.errors.append('Username is used!')
			result = False

		user = User.query.filter_by(email=self.email.data).first()
		if user is not None:
			self.email.errors.append('Email is used!')
			result = False
		return result
