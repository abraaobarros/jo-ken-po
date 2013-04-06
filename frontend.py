# coding: utf-8

import json
from util import session_module
from index import render

# internacionalização ==========================================================
from webapp2_extras import i18n
import jinja2
import os
jinja_environment = jinja2.Environment(
    extensions=['jinja2.ext.i18n'],
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
jinja_environment.install_gettext_translations(i18n)
# ==============================================================================


class MainHandler(session_module.BaseSessionHandler):
    def get(self):
        render(self, template_name="/home/index.html")


# >>> MACACO <<<
class PedidoController(session_module.BaseSessionHandler):
    def post(self):
        response = {}
        if self.session.get("mesa"):
            pedido = self.salvar_novo_pedido(
                self.request.get("id_item"),
                self.request.get("qtd"),
                self.request.get("observacao"),
                self.session.get("mesa"))
            if self.session.get("pedidos"):
                array_new = self.session["pedidos"]
                array_new.append(pedido.key().id_or_name())
                self.session["pedidos"] = array_new
            else:
                self.session["pedidos"] = [pedido.key().id_or_name()]
                str(pedido.idEstabelecimento),
                pedido.toJson()
            response = {"status": "ok"}
            self.response.out.write(json.dumps(response))
        else:
            response = {"status": "mesa"}
            self.response.out.write(json.dumps(response))


class CardapioController(session_module.BaseSessionHandler):
    """ Exibe a lista de Categorias do local"""
    def get(self, id_est_str):
        if self.session.get("user_id"):
            pass
        else:
            self.redirect("/login/"+id_est_str)
