import json
import string
import random
import time
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
        res = {}
        for url in urls:
            res[url.id] = {
                'url': url.url,
                'alias': url.alias,
            }
        return jsonify(res)

    @app.route('/u/urlencurt/<id>', methods = ['GET'])
    def get(id):   
        urlreturn = UrlEncurt.query.get(id)
        res = {
            'urlencurt': '/u/urlencurt/' + urlreturn.alias,
            'urloriginal': urlreturn.url,
            }

        return jsonify(res)

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

        coisa = UrlEncurt(url, alias)

        db.session.add(coisa)
        db.session.commit()
        end = time. time()
        finaltime= str(end-start)
        return jsonify({coisa.id: {
            'urloriginal': coisa.url,
            'alias': coisa.alias,
            'urlencurtada': '/u/urlencurt/' + coisa.alias,
            "statistics": {
                       "time_taken": finaltime,
            }
        }})

#urlEncurt_view =  UrlEncurtView.as_view('urlEncurt_view')
#app.add_url_rule(
#    '/u/url/', view_func=urlEncurt_view, methods=['POST']
#)

    #def put(self, id):
    #    # Update the record for the provided id
    #    # with the details provided.
    #    return



#@app.route('/contact')
#def contact():
#    """Renders the contact page."""
#    return render_template(
#        'contact.html',
#        title='Contact',
#        year=datetime.now().year,
#        message='Your contact page.'
#    )

#@app.route('/about')
#def about():
#    """Renders the about page."""
#    return render_template(
#        'about.html',
#        title='About',
#        year=datetime.now().year,
#        message='Your application description page.'
#    )
