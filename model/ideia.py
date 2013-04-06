from google.appengine.ext import db
from model.Usuario import Usuario


class Ideia (db.Model):
    nome = db.StringProperty()
    descricao = db.TextProperty()
    video = db.StringProperty()
    categoria = db.StringProperty()

    usuario = db.ReferenceProperty(Usuario, collection_name='ideias')
    votos = db.IntegerProperty()
    lista_usuarios = db.ListProperty(db.Key)
