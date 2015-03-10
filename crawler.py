import pprint
import logging

from fbgraph import FBGraphController
from neo4jgraph import N4JGraphController

#TODO: Use threads!
class Crawler:
    fb = None
    n4j = None
    queue = []
    depth_level = 1

    def __init__(self, config):        
        self.fb  = FBGraphController(config['fb-api'])
        self.n4j = N4JGraphController(config['neo4j'])
        self.queue = config['crawler']['root_sites']
        self.depth_level = config['crawler']['depth_level']
        if config['crawler']['reset_graph']:
            self.n4j.delete_all()

    def get_and_store_page(self, page_id):
        page = self.fb.get_page(page_id)
        return self.n4j.add(page)
    
    def crawl_page_likes(self, page_id):
        page_node = self.get_and_store_page(page_id)
        liked_pages = self.fb.get_liked_pages(page_id)
        for liked_page in liked_pages:
            liked_page_node = self.n4j.add(liked_page)
            self.n4j.add_relation(page_node, 'LIKES', 
                                  liked_page_node)
            logging.info('Queueing ' + liked_page['fb_id'])
            self.queue.append(liked_page['fb_id'])

    def recursive_crawling(self):
        for level in range(0, self.depth_level):
            current_queue = list(self.queue)
            self.queue[:] = []
            for page_id in current_queue:
                if not self.n4j.page_exists(page_id):
                    self.crawl_page_likes(page_id)
