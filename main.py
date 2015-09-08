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
	if str.split(' ', 1)[0] == "ocvs":
		return "https://github.com/Itseez/opencv/search?q=\"" + \
		str.split(' ', 1)[1] + "\""
	else:
		return "http://www.google.com/search?q="+str

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
