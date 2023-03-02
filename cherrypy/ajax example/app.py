#!/usr/bin/env python
#
# https://stackoverflow.com/questions/25634630/how-to-call-a-python-script-with-ajax-in-cherrypy-app


import os

import cherrypy
from cherrypy.lib.static import serve_file


path = os.path.abspath(os.path.dirname(__file__))
config = {
    'global': {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'server.thread_pool': 8
    }
}


class App:

    @cherrypy.expose
    def index(self):
        return serve_file(os.path.join(path, 'index.html'))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getData(self):
        return {
            'foo': 'bar',
            'baz': 'another one'
        }


if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config)
