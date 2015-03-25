from django.shortcuts import render
#FIXME: Check the best way to import this modules, aware of other apps
from neo4jgraph import N4JGraphController
import yaml
import logging

def index(request):
    #FIXME: Make config and n4jGraph persistent
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    config   = yaml.load(file('../config.yaml', 'r'))
    n4jGraph = N4JGraphController(config['neo4j'])
    pages = n4jGraph.get_pages(10)
    context = {'pages': pages}
    return render(request, 'tag_page/index.html', context)
