# coding: utf-8

import webapp2
import jinja2
import os
import logging
from util import session_module
from model.Usuario import Usuario
from model.ideia import Ideia
# import gdata.youtube.service

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


def render(handler, template_name="index.html", values={}):
    """ Método utilizado para renderizar a template passada através da variável 'template_name',
    usando os valores especificados pelo dict 'values'. Já 'handler' é uma referência ao
    Handler específico que fez a chamada do método. """

    # recupera o caminho do arquivo a ser exibido e adiciona seu nome
    # o caminho no caso do jinja jah eh relativo
    template_file = os.path.join(
        "templates/" + template_name)
    # verifica se o arquivo existe
    if not os.path.isfile(template_file):
        return False

    # copia o dict e adiciona o caminho do arquivo que fez a request
    copia_values = dict(values)
    copia_values['path'] = handler.request.path

    # gera a pagina
    template = jinja_environment.get_template(template_file)
    output_string = template.render(copia_values)
    handler.response.out.write(output_string)
    return True


class MainHandler(session_module.BaseSessionHandler):
    def get(self):
        

        # service = gdata.youtube.service.YouTubeService()
        # feed_url = 'http://gdata.youtube.com/feeds/api/standardfeeds/most_viewed?v=2'
        # feed = service.GetYouTubeVideoFeed(feed_url)
        # entry = feed.entry[0] # pick most viewed video as sample entry

        # thumbnail = entry.media.thumbnail[0].url

        ideias = Ideia.all()
        dados = {
            'ideias': ideias,
            'email': self.session.get("email"),
        }
        render(self, template_name='index.html', values=dados)


class LoginHandler(session_module.BaseSessionHandler):
    def get(self):
        if self.request.get('logout') == 'true':
            if self.session.get('email') is not None:
                self.session.pop("email")
            render(self, 'login.html')

    def post(self):
        if self.session.get('email') is None:
            logging.warning("Iniciando login")
            username = self.request.get('username')
            password = self.request.get('password')
            dados = {
                'username': username,
                'password': password,
            }
            logging.warning(dados)
            msg = Usuario.validar_login(dados)
            if msg is None:
                logging.warning("Logou")
                self.session['email'] = username
                render(self)
            else:
                logging.warning("Não logou"+str(msg))
                render(self, 'login.html')
        else:
            render(self)


class CadastroHandler(session_module.BaseSessionHandler):
    def get(self):
        render(self, template_name='cadastro.html')

    def post(self):
        logging.warning("Sessão: " + str(self.session.get('email')))
        if self.session.get('email') is None:
            logging.warning("Pegando as variáveis do GET")
            nome = self.request.get('nome')
            username = self.request.get('username')
            password = self.request.get('password')
            conf_password = self.request.get('conf_password')
            dados = {
                'username': username,
                'password': password,
                'conf_password': conf_password,
            }
            msg = Usuario.validar_cadastro_usuario(dados)
            if msg is None:
                logging.warning(u"Salvando no banco")
                usuario = Usuario(key_name=username)
                usuario.nome = nome
                usuario.username = username
                usuario.password = usuario.senha_md5(password)
                usuario.put()
                logging.warning("Salvo no banco")
                self.session['email'] = username
                render(self)
            else:
                render(self, template_name='cadastro.html', values={'erro': msg})
        else:
            render(self)


class CadastrarIdeiaHandler(session_module.BaseSessionHandler):
    def get(self):
        render(
            self,
            template_name="cadastrar_ideia.html",
            values={'email': self.session.get('email')})

    def post(self):
        nome = self.request.get('nome')
        descricao = self.request.get('descricao')
        video = self.request.get('video')
        categoria = self.request.get('categoria')

        ideia = Ideia()
        ideia.nome = nome
        ideia.descricao = descricao
        ideia.video = video
        ideia.categoria = categoria
        #ideia.usuario = Usuario.get_by_key_name(self.session.get('email'))
        ideia.votos = 0
        ideia.put()

        self.redirect("/")



class ListaIdeiasHandler(session_module.BaseSessionHandler):
    def get(self):
        if self.session.get("email") is not None:
            ideias = Ideia.all()
            dados = {
                'ideias': ideias,
                'email': self.session.get("email"),
            }
            render(self, template_name="lista_ideias.html", values=dados)
        else:
            render(self)

    def post(self):
        if self.session.get("email") is not None:
            usuario = Usuario.get_by_key_name(self.session.get("email"))
            usuario.votar()
            usuario.put()
        else:
            render(self)

class IdeiaHandler(session_module.BaseSessionHandler):
    def get(self, ideia_id):
            ideia = Ideia.get_by_id(long(ideia_id))
            dados = {
                'ideia': ideia,
            }
            render(self, template_name="ideia.html", values=dados)

class VotarHandler(session_module.BaseSessionHandler):
    def post(self):
            ideia = Ideia.get_by_id(long(self.request.get("ideia")))
            if ideia.votos is None:
                ideia.votos = 0
            ideia.votos = ideia.votos+1
            ideia.put()
            self.response.out.write(ideia.votos)
            # dados = {
            #     'ideia': ideia,
            # }
            # render(self, template_name="ideia.html", values=dados)

app = webapp2.WSGIApplication(
    [
        ('/', MainHandler),
        ('/login', LoginHandler),
        (r'/ideia/(\d+)', IdeiaHandler),
        ('/ideias', ListaIdeiasHandler),
        ('/votar', VotarHandler),
        ('/cadastro', CadastroHandler),
        ('/cadastrar_ideia', CadastrarIdeiaHandler),
    ],
    debug=True,
    config=session_module.myconfig_dict)


#TODO: talvez não precise...
class CadastrarProjetoHandler(session_module.BaseSessionHandler):
    def get(self):
        if self.session.get("email") is None:
            render(self, template_name="login.html")
        else:
            render(self, template_name="cadastrar_projeto.html")

    def post(self):
        pass


class ListaProjetosHandler(session_module.BaseSessionHandler):
    def get(self):
        pass
#===============================================================================
