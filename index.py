# coding: utf-8

import webapp2
import jinja2
import os

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


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('dsadasda')


app = webapp2.WSGIApplication(
    [
        ('/', MainHandler),
    ],
    debug=True)
