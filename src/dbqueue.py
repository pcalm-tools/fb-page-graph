import pprint
import logging
import sqlite3

logger = logging.getLogger('dbqueue')
logger.setLevel(logging.WARN)

class DBQueue:
    def __init__(self, config):
        self.conn = sqlite3.connect(config['file'])
        self.cursor = self.conn.cursor()
        self.STATUS_FAILED  = 1
        self.STATUS_CRAWLED = 2
        self.STATUS_QUEUED  = 3
            
    def enqueue(self, page_id):
        logger.info('Enqueueing %s' % (str(page_id)))
        self.cursor.execute(''' INSERT OR REPLACE INTO fb_page
            (fb_id, status_id) VALUES (?,?)''', (page_id, self.STATUS_QUEUED))
        self.conn.commit()

    def mark_crawled(self, page):
        logger.info('Crawled %s (%s)' % (str(page['fb_id']), page['name']))
        self.cursor.execute(''' INSERT OR REPLACE INTO fb_page
        (fb_id, username, name, about, description, status_id)
        VALUES (?,?,?,?,?,?)''',
        (page['fb_id'], page.get('username', ''), page.get('name', ''), 
         page.get('about', ''), page.get('description', ''), self.STATUS_CRAWLED))
        self.conn.commit()

    def mark_failed(self, page_id):
        logger.info('Failed %s' % (str(page_id)))
        self.cursor.execute(''' INSERT OR REPLACE INTO fb_page
            (fb_id, status_id) VALUES (?,?)''', (page_id, self.STATUS_FAILED))
        self.conn.commit()

    def reset(self):
        logger.warn('Deleting table fb_pages')
        self.cursor.execute(''' DELETE FROM fb_page ''')
        self.conn.commit()
