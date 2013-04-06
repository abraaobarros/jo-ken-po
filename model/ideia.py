from google.appengine.ext import db

class Ideia (db.Model):
    nome = db.StringProperty()
    descricao = db.TextProperty()
    video = db.StringProperty()
    usuario = db.ReferenceProperty(Usuario, collection_name='ideias')
    categoria = db.StringProperty()
    votos = db.IntegerProperty()
    lista_usuarios = db.ListProperty(db.key)