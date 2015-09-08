from flask.views import View
from flask import request, redirect
from app import models, app

@app.route('/')
def home():
	if 'q' in request.args:
		item = models.commands.Commands.query.filter_by(cmd_id=request.args.get('q').split(' ')[0]).first()
		if item is None:
			return redirect('http://www.google.com/search?q=%s' % request.args.get('q'), code=302)
		else:
			data = item.url
			return redirect(data.replace('%s', request.args.get('q').split()[1]), code=302)
	else:
		return "Under Construction"

