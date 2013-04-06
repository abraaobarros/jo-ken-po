# coding: utf-8

import webapp2
from webapp2_extras import sessions


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
