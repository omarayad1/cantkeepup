from flask.views import View
from flask import request, redirect
from app import models, app

@app.route('/')
def home():
	if 'q' in request.args:
		query = request.args.get('q')
		try:
			cmd_id = query.split(' ', 1)[0]
		except Exception, e:
			cmd_id = ""

		try:
			queryText = query.split(' ', 1)[1]
		except Exception, e:
			queryText = ""

		item = models.command.Command.query.filter_by(cmd_id=cmd_id).first()

		if item is None:
			return redirect('http://www.google.com/search?q=%s' % \
					query, code=302)
		else:
			data = item.url
			return redirect(data.replace('%s', queryText), code=302)
	else:
		return "Under Construction"