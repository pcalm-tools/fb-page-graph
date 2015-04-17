import pprint
import logging
import time

from fbgraph    import FBGraphController
from neo4jgraph import N4JGraphController
from dbqueue    import DBQueue

logger = logging.getLogger('crawler')
logger.setLevel(logging.INFO)

#TODO: Use threads!
class Crawler:
    def __init__(self, config):
        self.fb          = FBGraphController(config['fb-api'])
        self.n4j         = N4JGraphController(config['neo4j'])
        self.dbqueue     = DBQueue(config['db-queue'])
        self.queue       = config['crawler']['root_sites']
        self.depth_level = config['crawler']['depth_level']
        if config['crawler']['reset_graph']:
            self.n4j.delete_all()
            self.dbqueue.reset()
        else:
            self.queue = self.n4j.get_leaf_pages()

    def get_and_store_page(self, page_id):
        page_node = None
        page = self.fb.get_page(page_id)
        if page:
            page_node = self.n4j.add(page)
            self.dbqueue.mark_crawled(page)
        else:
            self.dbqueue.mark_failed(page_id)
        return page_node

    def crawl_page_likes(self, page_id):
        page_node = self.get_and_store_page(page_id)
        if page_node:
            liked_pages = self.fb.get_liked_pages(page_id)
            logger.info('%d pages liked' % (len(liked_pages)))
            for liked_page in liked_pages:
                liked_page_node = self.n4j.add(liked_page)
                self.n4j.add_relation(page_node, 'LIKES', liked_page_node)
                self.queue.append(liked_page['fb_id'])
                self.dbqueue.enqueue(liked_page['fb_id'])
                
    def crawl(self):
        for level in range(0, self.depth_level):
            current_queue = list(self.queue)
            self.queue[:] = []
            for page_id in current_queue:
#                if not self.n4j.page_exists(page_id):
                logger.info("[L%d] %s ..." % (level, str(page_id)))
                self.crawl_page_likes(page_id) 
                    #time.sleep(1)
                #else:
                 #   logger.info("[L%d] %s * skipped * " % (level, str(page_id)))
