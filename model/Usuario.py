# coding: utf-8
from google.appengine.ext import db
import logging


class Usuario(db.Model):
    nome = db.StringProperty()
    username = db.StringProperty()
    password = db.StringProperty()
    id_facebook = db.StringProperty()

    @classmethod
    def validar_cadastro_usuario(self, dados):
        msg = ""
        username = dados['username']
        password = dados['password']
        conf_password = dados['conf_password']
        logging.warning("Username: " + str(username))
        logging.warning("Password: " + str(password))
        logging.warning("Conf-Password: " + str(conf_password))
        if username == u"":
            msg = u"Formulário vazio"
        elif (password == u"") or (conf_password == u""):
            msg = u"Senha não pode ser vazia"
        elif password == conf_password:
            usuario = Usuario.get_by_key_name(username)
            logging.warning("Usuario: " + str(usuario))
            if usuario is None:
                novo_usuario = Usuario(key_name=username)
                novo_usuario.password = password
                novo_usuario.put()
                msg = None
            else:
                msg = u"Usuário já existe"
        else:
            msg = u"Senhas não conferem"
        logging.warning(msg)
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
                logging.warning("Tipo do self: " + str(self))
                password_md5 = usuario.senha_md5(password)
                if usuario.password == password_md5:
                    msg = None
                else:
                    msg = u"Senha incorreta"
        return msg

    def senha_md5(self, senha):
        import hashlib
        senha_md5 = hashlib.md5(senha).hexdigest()
        return senha_md5

    def votar(self):
        logging.warning(dir(self.ideias))
        self.ideias += 1
