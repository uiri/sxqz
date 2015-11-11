import os, re, json
import urllib2, urllib
from flask import Flask, request, render_template, send_from_directory
from flask import redirect as redirect
app = Flask(__name__)
shortcuts = { 	"a" : "amazon.com/s/?field-keywords=",
                "b" : "bing.com/search?q=",
                "d" : "duckduckgo.com/?q=",
                "e" : "www.ebay.com/sch/items/?_nkw=",
                "f" : "www.google.com/finance?q=",
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
        query = query.replace('+', '%2B')
        query = urllib.quote_plus(query[1:])
        wolframalpha = "http://wolframalpha.com/input/?i=" + query
        return redirect(wolframalpha)
    elif re.search("^/r/", query):
        subreddit = "http://reddit.com"+query
        return redirect(subreddit)
    elif re.search("/[A-Za-z]$", query):
        short = query[-1]
        query = query[:-2]
        if query == '':
            if short == 'q':
                surl = 'http://quora.com'
            elif short == 'f':
                surl = "http://www.google.com/finance"
            else:
                surl = "http://" + shortcuts[short].split('/')[0]
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
            mapurl = "http://google.com/maps/?force=lite&q=" + urllib.quote_plus(query)
            return redirect(mapurl)
        elif re.search("//img$", query):
            query = query.replace("//img", "")
            imgurl = "http://google.com/search?tbm=isch&q=" + urllib.quote_plus(query)
            return redirect(imgurl)
        elif re.search("//archive$", query):
            query = query.replace("//archive", "")
            archurl = "http://wayback.archive.org/web/" + query
            return redirect(archurl)
        elif re.search("//code(;l=[A-Za-z]+)?$", query):
            if re.search("//code$/", query):
                params = ""
            else:
                paramslist = re.findall("//code;l=([A-Za-z]+)$", query)
                params = "&Language=" + paramslist[0][1]
            query = query.split("//")[0]
            codeurl = "http://github.com/search?type=Code" + params + "&q=" + query
            return redirect(codeurl)
        elif re.search("//translate(\|[A-Za-z][A-Za-z])*$", query):
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
        elif re.search("^[0-9]+//rfc$", query):
            query = query.replace("//rfc", "")
            rfcurl = "http://tools.ietf.org/html/rfc"+query
            return redirect(rfcurl)
        elif re.search("^[0-9]+//xkcd$", query):
            query = query.replace("//xkcd", "")
            xkcdurl = "http://xkcd.com/"+query+"/"
            return redirect(xkcdurl)
        elif re.search("^//rand$", query):
            return redirect("http://en.wikipedia.org/wiki/Special:Random")
        else:
            subquery = ""
            if re.search("^//", query):
                if '/' in query[2:]:
                    qsplitslash = query[2:].split('/', 1)
                    subquery = qsplitslash[1]
                    query = "//" + qsplitslash[0]
            if not re.search("\.[A-Za-z]{2,4}$", query):
                if re.search("\.o$", query):
                    query += "rg"
                elif re.search("\.n$", query):
                    query += "et"
                elif re.search("\.$", query):
                    query += "com"
                else:
                    query += ".com"
            if re.search("^//.com$", query):
                query = ""
            elif re.search("^//", query):
                newurl = "http:" + query + "/" + subquery
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
    bing = "http://google.com/search?q=" + urllib.quote_plus(query)
    return redirect(bing)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 2099))
    app.run(host='0.0.0.0', port=port)
