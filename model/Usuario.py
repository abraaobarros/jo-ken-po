# coding: utf-8
from google.appengine.ext import db


class Usuario(db.Model):
    nome = db.StringProperty()
    ideia = db.ReferenceProperty()
    username = db.StringProperty()
    password = db.StringProperty()
    id_facebook = db.StringProperty()

    @classmethod
    def validar_cadastro_usuario(self, dados):
        msg = ""
        username = dados['username']
        password = dados['password']
        conf_password = dados['conf_password']
        if username == u"":
            msg = u"Formulário vazio"
        elif (password == u"") or (conf_password == u""):
            msg = u"Senha não pode ser vazia"
        elif password == conf_password:
            usuario = Usuario.get_by_key_name(username)
            if usuario is None:
                usuario = Usuario(key_name=username)
                usuario.password = password
                usuario.put()
                msg = None
            else:
                msg = u"Usuário já existe"
        else:
            msg = u"Senhas não conferem"
        return msg

    @classmethod
    def validar_login(self, dados):
        msg = ""
        username = dados['username']
        password = dados['password']
        if username == u"":
            msg = u"Formulário vazio"
        elif password == u"":
            msg = u"Senha não pode ser vazia"
        else:
            usuario = Usuario.get_by_key_name(username)
            if usuario is None:
                msg = u"Usuário não existe"
            else:
                if usuario.password == self.senha_md5(password):
                    msg = None
                else:
                    msg = u"Senha incorreta"
        return msg

    def senha_md5(self, senha):
        import hashlib
        senha_md5 = hashlib.md5(senha).hexdigest()
        return senha_md5
