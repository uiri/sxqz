import os, re, json
import urllib2, urllib
from flask import Flask, redirect, request
app = Flask(__name__)

@app.route('/')
def index():
    returnfile = open("home.tpl", 'r')
    returnstr = returnfile.read()
    print "hi"
    return returnstr

@app.route('/search')
def search():
    query = urllib.unquote_plus(request.args.get('q', ''))
    if re.search("^=", query):
        wolframalpha = "http://wolframalpha/input/?i=" + urllib.quote_plus(query[1:])
        return redirect(wolframalpha)
    else:
        wikiurl = "https://en.wikipedia.org/w/api.php?format=json&action=query&titles=" + query
        #request = urllib2.Request(url=wikiurl, headers={'User-Agent': 'Pass-Thrust'})
        wikijson = urllib2.urlopen(wikiurl).read()
        res = json.loads(wikijson)
        if int(res[u'query'][u'pages'].keys()[0]) != -1:
            wikipedia = "http://en.wikipedia.org/wiki/" + urllib.quote_plus(query)
            return redirect(wikipedia)
        else:
            bing = "http://bing.com/search?q=" + urllib.quote_plus(query)
            return redirect(bing)
    #return "hi"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
