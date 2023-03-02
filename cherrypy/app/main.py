#!/usr/bin/env python3
#
# https://docs.cherrypy.org/en/latest/tutorials.html#tutorial-6-what-about-my-javascripts-css-and-images


import os.path
import sys
import cherrypy
import json


class IndexPage:

    @cherrypy.expose
    def index(self):
        # Ask for the user's name.
        with open("res/index.html", "r") as f:
            s = f.read()
        return s                              # serving a string
        #return open("res/index.html", "r")   # serving an open file

    @cherrypy.expose
    def greetUser(self, name=None):
        # test user name.  If defined, say hoi.
        if name:
            # Greet the user!
            return "Hoi %s, what's up?" % name
        else:
            if name is None:
                # No name was specified
                return 'Please enter your name <a href="./">here</a>.'
            else:
                return 'No, really, enter your name <a href="./">here</a>.'

    @cherrypy.expose
    def changeParagraph(self, text='whatever'):
        # called by Javascript
        print('Javascript call: ' + text)
        if text == 'array':
            lst = [
                    ["sub_title", "Hello students"],
                    ["par_1", "This is an example of JSON, JS, and DOM."],
                    ["par_2", "Pretty neat."]
                    ];
            return json.dumps(lst)
        else:
            return(text)

mainconf = os.path.join(os.path.dirname(__file__), 'main.conf')

conf = {
    'global':{
        'server.socket_host': "127.0.0.1",
        'server.socket_port': 8080,
        'server.thread_pool': 10
        },
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './res'
    }
}


def main(arg):
    #cherrypy.quickstart(IndexPage(), config=mainconf)
    #cherrypy.quickstart(IndexPage(), "/", conf)
    cherrypy.quickstart(IndexPage(), "/", conf)
    return


if __name__ == "__main__":
    main(sys.argv)
