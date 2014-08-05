import os
import json
import requests

import flask
from flask import Flask

app = Flask(__name__)
cache = {}
imgcache = {}

@app.route('/')
def hello():
	# return "dog"
	return open("main.html", 'r').read()

@app.route('/api')
def api():
	data = json.dumps({"a":"b"})
	r = flask.make_response( data )
	r.mimetype = 'application/json'
	return r

@app.route('/img')
def img():
        global imgcache
        l = flask.request.args.get('url',None)
        if l:
                if l in imgcache:
                        c = imgcache[l]
                else:
                        c = requests.get(l).content
                        imgcache[l] = c
                r1 = flask.make_response(c)
                r1.mimetype = 'image/jpeg'
                return r1
        else:
                return "provide parameter: url"

@app.route('/links')
def links():
        global cache
        title = flask.request.args.get('title','gorilla')
        if (title in cache) and (len(cache[title]) > 10):
                rr = cache[title]
        else:
                r = requests.get('http://www.myapifilms.com/imdb?title=%s&exactFilter=0&limit=10'%(title,))
                rc = r.text
                j = json.loads(rc)
                for jj in j:
                        jj['urlPoster'] = '/img?url='+jj['urlPoster']
                rr = json.dumps(j)
                cache[title] = rr
	r1 = flask.make_response(rr)
	r1.mimetype = 'application/json'
	return r1

if __name__ == '__main__':
    app.run(debug=True)
