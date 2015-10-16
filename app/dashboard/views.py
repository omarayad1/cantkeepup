from flask import Blueprint, render_template, flash, url_for, redirect, \
		jsonify # pragma: no cover
from flask.ext.login import login_required, current_user, request \
		 # pragma: no cover
from app.models import Command, Group  # pragma: no cover
from forms import CommandForm # pragma: no cover
from app import db # pragma: no cover
from app.core.helpers import queryAllToJson, objectToJson # pragma: no cover
from sqlalchemy.exc import IntegrityError # pragma: no cover

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

@dashboard_blueprint.route('/dashboard') # pragma: no cover
@login_required # pragma: no cover
def dashboard():
	global_group = Group.query.filter_by(groupname='global').first()
	global_commands = Command.query.filter_by(owner=global_group.id)
	return render_template('dashboard.html', global_commands=global_commands)

@dashboard_blueprint.route('/dashboard/_addusercommand', methods=['POST']) \
		 # pragma: no cover
@login_required  # pragma: no cover
def addusercommand():
	cmd_id = request.form.get('cmd_id', None, type=str)
	url = request.form.get('url', None, type=str)
	name = request.form.get('name', None, type=str)
	if cmd_id == "" or url == "" or name == "" or \
		cmd_id is None or url is None or name is None:
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
		db.session.rollback()
		return 'Command ID already exists', 400
	except Exception as e:
		db.session.rollback()
		return 'Unexpected Error', 400

@dashboard_blueprint.route('/dashboard/_updateusercommand', methods=['POST']) \
		 # pragma: no cover
@login_required # pragma: no cover
def updateusercommand():
	cmd_id = request.form.get('cmd_id', None, type=str)
	url = request.form.get('url', None, type=str)
	name = request.form.get('name', None, type=str)

	if cmd_id == "" or url == "" or name == "" or \
		cmd_id is None or url is None or name is None:
		return 'A value is missing', 400

	conditions = {'owner':current_user.get_id(), 'cmd_id':cmd_id}
	updates = {}
	if url is not None: updates['url'] = url
	if name is not None: updates['name'] = name
	try:
		db.session.query(Command).filter_by(**conditions).update(updates)
		db.session.commit()
		return objectToJson(Command.query.filter_by(**conditions).first()), 200
	except Exception as e:
		db.session.rollback()
		return 'Unexpected Error', 400

@dashboard_blueprint.route('/dashboard/_deleteusercommand', methods=['POST']) \
		 # pragma: no cover
@login_required # pragma: no cover
def deleteusercommand():
	cmd_id = request.form.get('cmd_id', None, type=str)
	if cmd_id == "" or cmd_id is None:
		return 'Command ID is missing.', 400
	conditions = {'owner':current_user.get_id(), 'cmd_id':cmd_id}

	try:
		Command.query.filter_by(**conditions).delete()
		db.session.commit()
		return 'success', 200
	except Exception as e:
		db.session.rollback()
		return 'Unexpected Error', 400

@dashboard_blueprint.route('/dashboard/_loadusercommands') \
		 # pragma: no cover
@login_required # pragma: no cover
def loadusercommands():
	cmd_id = request.args.get('cmd_id', None, type=str)
	url = request.args.get('url', None, type=str)
	name = request.args.get('name', None, type=str)
	conditions = {'owner':current_user.get_id()}
	if cmd_id != None and cmd_id != "": conditions['cmd_id'] = cmd_id
	if url != None and url != "": conditions['url'] = url
	if name != None and name != "": conditions['name'] = name
	try:
		return queryAllToJson(Command,conditions), 200
	except Exception as e:
		db.session.rollback()
		return 'Unexpected Error', 400

@dashboard_blueprint.route('/dashboard/addcommand', methods=['GET', 'POST']) \
		 # pragma: no cover
@login_required # pragma: no cover
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
