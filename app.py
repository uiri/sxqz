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
    query = query.replace(' //', '//')
    if re.search("^=", query):
        wolframalpha = "http://wolframalpha/input/?i=" + urllib.quote_plus(query[1:])
        return redirect(wolframalpha)
    elif re.search("//", query):
        #if re.search("/[A-Za-z]$", query):
            #stuff
        #if re.search("//define$", query):
            #stuff
        if re.search("//map$", query):
            query = query.replace("//map", "")
            mapurl = "http://google.com/maps?q=" + urllib.quote_plus(query)
            return redirect(mapurl)
        elif re.search("//img$", query):
            query = query.replace("//img", "")
            imgurl = "http://google.com/search?tbm=isch&q=" + urllib.quote_plus(query)
            return redirect(imgurl)
        elif re.search("//code(;l=[A-Za-z]+)?$", query):
            if re.search("//code$/", query):
                params = ""
            else:
                paramslist = re.findall("//code;l=([A-Za-z]+)$", query)
                params = "&Language=" + paramslist[0][1]
            query = query.split("//")[0]
            codeurl = "http://github.com/search?type=Code" + params + "&q=" + query
            return redirect(codeurl)
        else:
            if not re.search("\.[A-Za-z]{2,4}$", query):
                if re.search("\.o$", query):
                    query += "rg"
                elif re.search("\.n$", query):
                    query += "et"
                elif re.search("\.$", query):
                    query += "com"
                else:
                    query += ".com"
            if re.search("^//", query):
                newurl = "http:" + query
                return redirect(newurl)
            else:
                query = query.replace("//", " site:")
    else:
        wikiurl = "https://en.wikipedia.org/w/api.php?format=json&action=query&titles=" + query
        #request = urllib2.Request(url=wikiurl, headers={'User-Agent': 'Pass-Thrust'})
        wikijson = urllib2.urlopen(wikiurl).read()
        res = json.loads(wikijson)
        if int(res[u'query'][u'pages'].keys()[0]) != -1:
            wikipedia = "http://en.wikipedia.org/wiki/" + urllib.quote_plus(query)
            return redirect(wikipedia)
    bing = "http://bing.com/search?q=" + urllib.quote_plus(query)
    return redirect(bing)
    #return "hi"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
