from flask.views import View # pragma: no cover
from flask import request, redirect, Blueprint, render_template \
		# pragma: no cover
from app import models, app # pragma: no cover
import urllib # pragma: no cover

home_blueprint = Blueprint(
	'home', __name__,
	template_folder='templates'
) # pragma: no cover


@home_blueprint.route('/') # pragma: no cover
def home():
	if 'q' in request.args:
		query = request.args.get('q')

		tokens = query.split(' ', 1)

		cmd_id = tokens[0]

		if len(tokens) > 1:
			queryText = tokens[1]
			queryText = urllib.quote(queryText.encode('utf8'), safe='')
		else:
			queryText = ""

		item = models.command.Command.query.filter_by(cmd_id=cmd_id).first()

		if item is None:
			query = urllib.quote(query.encode('utf8'), safe='')
			return redirect('http://www.google.com/search?q=%s' % \
					query, code=302)
		else:
			data = item.url
			return redirect(data.replace('%s', queryText), code=302)
	else:
		return render_template('index.html')
