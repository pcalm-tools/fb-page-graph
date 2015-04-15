import pprint
import logging
import time

from fbgraph import FBGraphController
from neo4jgraph import N4JGraphController

#TODO: Use threads!
class Crawler:
    fb          = None
    n4j         = None
    queue       = []
    depth_level = 1

    def __init__(self, config):        
        self.fb          = FBGraphController(config['fb-api'])
        self.n4j         = N4JGraphController(config['neo4j'])
        self.queue       = config['crawler']['root_sites']
        self.depth_level = config['crawler']['depth_level']
        if config['crawler']['reset_graph']:
            self.n4j.delete_all()
        else:
            self.queue = self.n4j.get_leaf_pages()

    def get_and_store_page(self, page_id):
        page_node = None
        try:
            page = self.fb.get_page(page_id)
            page_node = self.n4j.add(page)
        except:
            print " *** Error getting " + str(page_id)
        return page_node

    def crawl_page_likes(self, page_id):
        page_node = self.get_and_store_page(page_id)
        if page_node:
            liked_pages = self.fb.get_liked_pages(page_id)
            for liked_page in liked_pages:
                liked_page_node = self.n4j.add(liked_page)
                self.n4j.add_relation(page_node, 'LIKES', 
                                      liked_page_node)
                logging.info('Queueing ' + liked_page['fb_id'])
                self.queue.append(liked_page['fb_id'])

    def run(self):
        for level in range(0, self.depth_level):
            current_queue = list(self.queue)
            self.queue[:] = []
            for page_id in current_queue:
                logging.info("Getting " + str(page_id))
                #TODO: IF page exists and have not children
                if not self.n4j.page_exists(page_id):
                    print "[Level %d]" % (level) + str(page_id)
                    self.crawl_page_likes(page_id) 
                    time.sleep(1)
                    print "[Level %d] Finished " % (level) + str(page_id)
                else:
                    print "[Level %d] Omitting " % (level) + str(page_id)