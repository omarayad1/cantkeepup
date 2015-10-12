from flask import Blueprint, render_template, flash, url_for, redirect \
		# pragma: no cover
from flask.ext.login import login_required, current_user, request
from app.models import Command, Group
from forms import CommandForm
from app import db

################
#### config ####
################

dashboard_blueprint = Blueprint(
	'dashboard', __name__,
	template_folder='templates'
) # pragma: no cover

################
#### routes ####
################

@dashboard_blueprint.route('/dashboard')
@login_required
def dashboard():
	user_commands = Command.query.filter_by(owner=current_user.id)
	global_group = Group.query.filter_by(groupname='global').first()
	global_commands = Command.query.filter_by(owner=global_group.id)
	return render_template('dashboard.html',user_commands=user_commands, \
			global_commands=global_commands)

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

