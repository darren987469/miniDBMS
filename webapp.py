# -*- coding: UTF-8 -*-
import cherrypy
import os
import json
from os import listdir
from os.path import isfile, join
from darren.main import executeCmd

class WebApp:
    # do the configuration
    ## get current path to avoid resetting when deploy somewhere else
    staticdir_root = os.path.dirname(os.path.abspath(__file__))
    _cp_config = {'tools.encode.encoding': 'utf-8',
                  'tools.staticdir.on' : True,
                  'tools.staticdir.dir' : staticdir_root,
                  'tools.staticdir.index' : 'index.html',
    }
    exposed = True
    
    @cherrypy.expose
    def tables(self, table=None):
        # return specified table
        if table:
            fname = table + ".txt"
            fpath = os.path.join(self.staticdir_root, "data", fname)
            print str(json.load(open(fpath)))
            return json.dumps(json.load(open(fpath)))
        # return tables list
        else:
            data_dir = os.path.join(self.staticdir_root,"data") 
            tables = [ f[:f.index(".")] for f in listdir(data_dir) if isfile(join(data_dir,f)) and f.endswith('.txt')]
            return json.dumps(tables) 
    
    @cherrypy.expose
    def query(self, query=None):
        if query:
            result = executeCmd(query)
            return json.dumps(result)
            
        

if __name__ == '__main__':
    #cherrypy.config.update({'server.socket_host': darren_url,'server.socket_port': 80,})
    cherrypy.quickstart(WebApp())
    pass