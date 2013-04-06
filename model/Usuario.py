from google.appengine.ext import db


class Usuario(db.Model):
    nome = db.StringProperty()
    username = db.StringProperty()
    senha = db.StringProperty()
    id_facebook = db.StringProperty()
