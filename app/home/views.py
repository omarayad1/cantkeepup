from flask.views import View # pragma: no cover
from flask import request, redirect, Blueprint, render_template \
		# pragma: no cover
from app import models, app # pragma: no cover
from app.core.commandprocessor import CommandProcessor

home_blueprint = Blueprint(
	'home', __name__,
	template_folder='templates'
) # pragma: no cover


@home_blueprint.route('/') # pragma: no cover
def home():
	if 'q' in request.args:
		commandProcessor = CommandProcessor(request.args.get('q'))
		return redirect(commandProcessor.processCommand(),code=302)
	else:
		return render_template('index.html')
