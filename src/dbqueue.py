import pprint
import logging
import sqlite3

logger = logging.getLogger('dbqueue')
logger.setLevel(logging.INFO)

class DBQueue:
    def __init__(self, config):
        self.conn = sqlite3.connect(config['db-file'])
        self.cursor = conn.cursor()
            
    def enqueue_page(self, page):
        self.cursor.execute(''' ''')

    def register_crawled_page(self, attributes):
        self.cursor.execute(''' ''')
