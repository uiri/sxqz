import os, re 
from urllib import urlencode, FancyURLopener
from flask import Flask, redirect
app = Flask(__name__)

class AppUrlOpener(FancyURLopener):
    version = "Pass-Thrust"

@app.route('/')
def index():
    returnfile = open("home.tpl", 'r')
    returnstr = returnfile.read()
    return returnstr

@app.route('/search/<query>')
def search(query):
    if re.match("=", query):
        query = urlencode(query)
        return redirect("http://wolframalpha.com/input/?i=" + query)
    else:
        wikiapi = AppUrlOpener.open("https://en.wikipedia.org/w/api.php?format=json&action=query&titles=" + query).read()
        return wikiapi

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
