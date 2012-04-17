import os, re, json
import urllib2, urllib
from flask import Flask, redirect, request, render_template, send_from_directory
app = Flask(__name__)
shortcuts = { 	"a" : "amazon.com/s/?field-keywords=",
                "b" : "bing.com/search?q=",
                "d" : "duckduckgo.com/?q=",
                "e" : "www.ebay.com/sch/items/?_nkw=",
                "g" : "google.com/search?q=",
                "q" : "google.com/search?q=site%3Aquora.com+",
                "r" : "reddit.com/search?q=",
                "s" : "soundcloud.com/search?q[fulltext]=",
                "t" : "thesaurus.com/browse/",
                "u" : "youtube.com/results?search_query=",
                "w" : "en.wikipedia.org/w/index.php?search=",
                "y" : "search.yahoo.com/search?p="                  }

@app.route('/favicon.png')
def favicon():
    return send_from_directory(app.root_path, 'favicon.png', mimetype='image/png')

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/search')
def search():
    query = urllib.unquote_plus(request.args.get('q', ''))
    if query == "":
        return index()
    query = query.replace(' //', '//')
    if re.search("^=", query):
        wolframalpha = "http://wolframalpha.com/input/?i=" + urllib.quote(query[1:])
        return redirect(wolframalpha)
    elif re.search("/[A-Za-z]$", query):
        short = query[-1]
        query = query[:-2]
        if query == '':
            if short != 'q':
                surl = "http://" + shortcuts[short].split('/')[0]
            else:
                surl = 'http://quora.com'
        else:
            surl = "http://" + shortcuts[short] + query
        return redirect(surl)
    elif re.search("//", query):
        if re.search("//define$", query):
            query = query.replace("//define", "")
            urbanurl = "http://urbandictionary.com/define.php?term=" + urllib.quote_plus(query)
            urbanfile = urllib2.urlopen(urbanurl)
            urbanhtml = urbanfile.read().split("<table id='entries'>")
            urbanhtml = urbanhtml[1].split("<!-- google_ad_section_end")
            urbanhtml = "<table>" + urbanhtml[0]
            urbanhtml = re.sub("\s(.+)\s<div class='greenery'>", "", urbanhtml)
            urbanhtml = re.sub("(\s)<a href=\"#(.+)\s", "\g<1>", urbanhtml)
            urbanhtml = re.sub("(\s)(.+)video\.php(.+)\s", "\g<1>", urbanhtml)
            urbanhtml = re.sub("\s(.+)\s(.+)\s$", "", urbanhtml)
            urbanhtml = re.sub("<script([^>]+)>\s//<([^<]+)</script>", "SCRIPT", urbanhtml)
            urbanhtml = re.sub("\s(.+)SCRIPT(.+)\s", "", urbanhtml)
            urbanhtml = re.sub("style='padding([^']+)'", "", urbanhtml)
            urbanhtml = re.sub("\s(.+)urbanup(.+)>(\d\.)<(.+)\s", "\g<3>", urbanhtml)
            urbanhtml = re.sub("/define\.php\?term=([^\"]+)", "/search?q=\g<1>//define", urbanhtml)
            urbanhtml = re.sub("/(author\.php\?author=[a-zA-Z0-9 ]+)", "//urbandictionary.com/\g<1>", urbanhtml)
            """            wikturl = "https://en.wiktionary.org/w/api.php?action=query&prop=revisions&rvprop=content&rvexpandtemplates=&format=json&titles=" + urllib.quote(query)
            wiktfile = urllib2.urlopen(wikturl)
            wiktjson = json.load(wiktfile)
            wiktkeys = wiktjson[u'query'][u'pages'].keys()
            wikthtmlobj = mwparser.WikiMarkup(s=wiktjson[u'query'][u'pages'][wiktkeys[0]][u'revisions'][0][u'*'].split("----")[0])
            wikthtml = wikthtmlobj.render()
            wikthtml = wikthtml.replace("&lt;\0", "<")
            wikthtml = wikthtml.replace("&rt;\0", ">") """
            return render_template("define.html", urb=urbanhtml, title=query)
        elif re.search("//map$", query):
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
        elif re.search("//translate$", query):
            query = query.replace("//translate", "")
            transurl = "http://translate.google.com/"
            if "|" in query:
                params = query.split("|")
                if len(params) == 2:
                    if params[1] == "en":
                        query = "#auto|" + params[1] + "|" + params[0]
                    else:
                        query = "#en|" + params[1] + "|" + params[0]
                else:
                    query = "#" + params[2] + "|" + params[1] + "|" + params[0]
            else:
                transurl += "#auto|en|"
            transurl += query
            return redirect(transurl)
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
                query = query.replace(" site:.com", "")
    else:
        wikiurl = "https://en.wikipedia.org/w/api.php?format=json&action=query&titles=" + urllib.quote(query)
        wikijson = urllib2.urlopen(wikiurl).read()
        res = json.loads(wikijson)
        if int(res[u'query'][u'pages'].keys()[0]) != -1:
            wikipedia = "http://en.wikipedia.org/wiki/" + urllib.quote(query)
            return redirect(wikipedia)
    bing = "http://bing.com/search?q=" + urllib.quote_plus(query)
    return redirect(bing)
    #return "hi"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
