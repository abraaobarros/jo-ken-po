# coding: utf-8
from google.appengine.ext import db
from model.ideia import Ideia
import logging


class Projeto(db.Model):
    nome = db.StringProperty()
    descricao = db.TextProperty()
    ideia = db.ReferenceProperty(Ideia)

# TODO: pensar nessa entidade depois.
