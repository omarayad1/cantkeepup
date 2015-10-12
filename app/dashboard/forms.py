from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class CommandForm(Form):
	cmd_id = TextField('Command ID', validators=[DataRequired()])
	name = TextField('Name', validators=[DataRequired()])
	url = TextField('URL', validators=[DataRequired()])