from Bemobi2 import db
 
class UrlEncurt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    numVisita = db.Column(db.Integer)
 
    def __init__(self, url, alias, numVisita):
        self.url = url
        self.alias = alias
        self.numVisita = numVisita
 
    def __repr__(self):
        return '<UrlEncurt %d>' % self.id


