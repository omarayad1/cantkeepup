from flask import Blueprint, render_template, flash, url_for, redirect, \
		jsonify # pragma: no cover
from flask.ext.login import login_required, current_user, request
from app.models import Command, Group
from forms import CommandForm
from app import db
from app.core.helpers import queryAllToJson, objectToJson
from sqlalchemy.exc import IntegrityError

################
#### config ####
################

dashboard_blueprint = Blueprint(
	'dashboard', __name__,
	template_folder='templates',
	static_folder='static',
	static_url_path='/dashboard/static'
) # pragma: no cover

################
#### routes ####
################

@dashboard_blueprint.route('/dashboard')
@login_required
def dashboard():
	global_group = Group.query.filter_by(groupname='global').first()
	global_commands = Command.query.filter_by(owner=global_group.id)
	return render_template('dashboard.html', global_commands=global_commands)

@dashboard_blueprint.route('/dashboard/_addusercommand')
@login_required
def addusercommand():
	cmd_id = request.args.get('cmd_id', None, type=str)
	url = request.args.get('url', None, type=str)
	name = request.args.get('name', None, type=str)
	if cmd_id == "" or url == "" or name == "":
		return 'A value is missing', 400

	try:
		command = Command(
			cmd_id=cmd_id,
			name=name,
			url=url,
			owner=current_user.id,
			creator=current_user.id
		)
		db.session.add(command)
		db.session.commit()
		return objectToJson(command), 200
	except IntegrityError:
		return 'Command ID already exists', 400
	except Exception as e:
		return 'Unexpected Error', 400

	return ''


@dashboard_blueprint.route('/dashboard/_loadusercommands')
@login_required
def loadusercommands():
	cmd_id = request.args.get('cmd_id', None, type=str)
	url = request.args.get('url', None, type=str)
	name = request.args.get('name', None, type=str)
	conditions = {'owner':current_user.get_id()}
	if cmd_id != None: conditions['cmd_id'] = cmd_id
	if url != None: conditions['url'] = url
	if name != None: conditions['name'] = name
	try:
		return queryAllToJson(Command,conditions), 200
	except Exception as e:
		return 'Unexpected Error', 400

	return ''

@dashboard_blueprint.route('/dashboard/addcommand', methods=['GET', 'POST'])
@login_required
def addcommands():
	form = CommandForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			command = Command(
				cmd_id=form.cmd_id.data,
				name=form.name.data,
				url=form.url.data,
				owner=current_user.id,
				creator=current_user.id
			)
			db.session.add(command)
			db.session.commit()
			flash('Command '+str(command)+' added successfully!')
			return redirect(url_for('dashboard.dashboard'))
	return render_template('addcommand.html', form=form)


