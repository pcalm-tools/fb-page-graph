import facebook
import pprint
import logging

class FBGraphController:
    """Access to common use Facebook Graph functionalities"""

    graph = None

    def __init__(self, config):
        self.graph = facebook.GraphAPI(config['access_token'])

    def get_page(self, page_id):
        logging.info('Getting page [' + page_id + ']')
        return self.graph.get_object(page_id)

    def get_liked_pages(self, page_id):
        liked_pages = []
        liked_page_ids = self.graph.get_connections(page_id, 'likes')

        for liked_page_id in liked_page_ids['data']:
            liked_pages.append(self.get_page(liked_page_id['id']))

        return liked_pages
        
