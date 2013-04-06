# coding: utf-8

import webapp2
from webapp2_extras import sessions
from model.UsuarioEstabelecimento import UsuarioEstabelecimento
from model.Usuario import Usuario
import logging


# dict necessário para configurar a chave secreta da sessão
myconfig_dict = {}
myconfig_dict['webapp2_extras.sessions'] = {
    'secret_key': '7h1s 1s m4d3 s0 7h47 n0b0dy gu3ss 0r 47 l1s7 h4v trouble'
}


class BaseSessionHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def md5_value(self, value):
        import hashlib
        return hashlib.md5(value).hexdigest()

    def login_backend_user(self, username, senha_md5):
        usuario = UsuarioEstabelecimento.all().filter('email =', username).filter('password =', senha_md5).get()
        if usuario is not None:
            self.session["id_est"] = usuario.idEstabelecimentoList.pop()
            self.session["usuario"] = usuario.nome
        self.redirect("/backend")

    def login_frontend_user(self, username, senha_md5):
        logging.warning(type(username))
        # Se for vazio ele recebe uma string vazia em unicode.
        if username is not u"":
            usuario = Usuario.get_by_key_name(username)
            if usuario is not None:
                if(usuario.password == senha_md5):
                    self.session["user_id"] = usuario.key().id_or_name()
                    return None
                else:
                    error = u"Password inválido"
                    return error
            else:
                error = u"Usuário inexistente"
                return error
        else:
            error = u"Por favor, insira alguma coisa"
            return error
