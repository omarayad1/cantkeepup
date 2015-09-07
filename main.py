from flask import request, Flask, redirect
import os
app = Flask(__name__)

@app.route('/')
def home():
    if 'q' in request.args:
        return redirect("http://www.google.com/search?q="+request.args.get('q'), code=302)
    else:
        return "Under Construction"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
