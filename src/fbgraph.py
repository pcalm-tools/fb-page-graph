import facebook
import pprint
import logging

logger = logging.getLogger('fbgraph')
logger.setLevel(logging.WARNING)

class FBGraphController:
    """Access to common use Facebook Graph functionalities"""

    def __init__(self, config):
        with open (config['access_token'], "r") as f:
            self.graph = facebook.GraphAPI(f.read())

    def get_page(self, page_id):
        try:
            page = self.graph.get_object(str(page_id))
            logger.info('Got page %s (%s)' % (str(page_id), page['name']))
        except facebook.GraphAPIError as e:
            logger.warn("** Error getting %s: %s" % (str(page_id), str(e)))
            page = None
        return page

    def get_liked_pages(self, page_id):
        liked_pages = []
        liked_page_ids = self.graph.get_connections(page_id, 'likes')

        for liked_page_id in liked_page_ids['data']:
            liked_pages.append(self.get_page(liked_page_id['id']))

        return liked_pages
        
