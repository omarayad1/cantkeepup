from flask import request, Flask, redirect
import os
app = Flask(__name__)

@app.route('/')
def home():
    if 'q' in request.args:
        return redirect(query(request.args.get('q')), code=302)
    else:
        return "Under Construction"

def query(str):
	try:
		command = str.split(' ', 1)[0]
	except Exception, e:
		command = ""

	try:
		queryText = str.split(' ', 1)[1]
	except Exception, e:
		queryText = ""

	if command == "ocvs":
		return "https://github.com/Itseez/opencv/search?q=\"" + \
			queryText + "\""
	elif command == 's' or command == 'g':
		return "http://www.google.com/search?q=" + queryText
	elif command == 't':
		return "https://translate.google.com/#en/ar/" + queryText
	elif command == 'p':
		return "https://pastie.org"
	elif command == 'ulib':
		return "http://aucegypt.summon.serialssolutions.com/search?s.q=" + \
			queryText
	else:
		return "http://www.google.com/search?q="+str

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
