import os
import re
import json
import urllib
import urllib2

env = os.environ

def redirect(uri):
    responseJson = {
        "status": 302,
        "headers": {
            "Location": uri
        },
        "body": ""
    }
    with open(env['res'], 'w') as responseFile:
        json.dump(responseJson, responseFile)

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

def search(req_param_q):
    query = urllib.unquote_plus(req_param_q)
    if query == "":
        return redirect("s.xqz.ca/")
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
        if re.search("//map$", query):
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

search(env['REQ_QUERY_Q'])