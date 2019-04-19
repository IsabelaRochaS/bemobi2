import json
import string
import random
import time
import webbrowser
from flask import request, jsonify, Blueprint, abort,render_template
from flask.views import MethodView
from Bemobi2 import db, app
from Bemobi2.model import UrlEncurt
from datetime import datetime

start = time. time()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

view = Blueprint('view', __name__)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return "Encurtador de URL's"

class UrlEncurtView(MethodView):
 
    @app.route('/u/urlencurt', methods = ['GET'])
    def getall():   
        urls = UrlEncurt.query.all()
        returnUrls = {}
        for url in urls:
            returnUrls[url.id] = {
                'urloriginal': url.url,
                'alias': url.alias,
                'urlencurt': '/u/urlencurt/' + url.alias,
            }
        return jsonify(returnUrls)

    @app.route('/u/urlencurt/<alias>', methods = ['GET'])
    def getByAlias(alias): 
        urlreturn = UrlEncurt.query.filter(UrlEncurt.alias == alias).first()

        if not urlreturn:
            returnUrl = {
                'alias': alias,   
                'err_code': "002",
                'description': "SHORTENED URL NOT FOUND",
                }
            return jsonify(returnUrl)

        urlopen = 'https://' + urlreturn.url
        webbrowser.open(urlopen)

        returnUrl = {
            'urlencurt': '/u/urlencurt/' + urlreturn.alias,
            'urloriginal': urlreturn.url,
            }

        return jsonify(returnUrl)

    @app.route('/u/urlencurt', methods = ['POST'])
    def post():
        url = request.json['url']
        alias = request.json['alias']

        if not alias:
            alias = id_generator()

        urls = UrlEncurt.query.all()
        for urlloop in urls:
            if urlloop.alias == alias:
                end = time. time()
                finaltime = str(end-start)
                return jsonify({
                    'alias' : alias,
                    'err_code': "001",
                    'description': "CUSTOM ALIAS ALREADY EXISTS",
                    "statistics": {
                       "time_taken": finaltime,
                    }
                })

        returnUrl = UrlEncurt(url, alias)

        db.session.add(returnUrl)
        db.session.commit()
        end = time. time()
        finaltime= str(end-start)
        return jsonify({returnUrl.id: {
            'urloriginal': returnUrl.url,
            'alias': returnUrl.alias,
            'urlencurtada': '/u/urlencurt/' + returnUrl.alias,
            "statistics": {
                       "time_taken": finaltime,
            }
        }})
