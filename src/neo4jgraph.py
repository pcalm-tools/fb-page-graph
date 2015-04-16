from py2neo import Graph, Node, Relationship, watch, schema, error
import pprint
import logging

logger = logging.getLogger('n4jgraph')
logger.setLevel(logging.WARNING)

class N4JGraphController:
    graph = None
    def __init__(self, config):
        # conn = "https://%s:%s@%s" % (config['user'], 
        #                             config['password'],
                                    # config['url'])

        conn = "http://%s" % (config['url'])
        self.graph = Graph(conn)
        self.initialize_schema()

    #TODO: Check if schema is not already created
    def initialize_schema(self):
        try:
            self.graph.schema.create_uniqueness_constraint('Page', 'fb_id')
            self.graph.schema.create_uniqueness_constraint('Page', 'username')
        except Exception as e:
            logger.info('Skipping creation of unique constraint')
            
    def add(self, page):
        #pprint.pprint(page)
        page = self.fix_format(page)
        logger.debug("Adding page %s (%s)" % (page['fb_id'], page['name']))
        node = self.graph.merge_one('Page', 'fb_id', page['fb_id'])
        node.properties.update(page)
        node.push()
        return node

    def add_relation(self, page1, relation, page2):
        logger.debug("Adding relation: %s -[%s]-> %s" %\
                     (page1['name'], relation, page2['name']))
        self.graph.create_unique(Relationship(page1, relation, page2))

    def delete_all(self):
        logger.warn('Deleting all nodes')
        self.graph.delete_all()

    def retrieve_page(self, page_id):
        page_node = self.graph.find_one('Page', 'fb_id', page_id)
        if page_node is None:
            page_node = self.graph.find_one('Page', 'username', page_id)
        return page_node

    def page_exists(self, page_id):
        return self.retrieve_page(page_id) is not None

    def fix_format(self, page):
        page['fb_id'] = page['id']
        page.pop('id')
        if 'cover' in page and type(page['cover']) is dict:
            if 'source' in page['cover']:
                page['cover'] = page['cover']['source']
        for key in page.keys():
            if type(page[key]) is dict or type(page[key]) is list:
                page.pop(key)
        return page

    def get_leaf_pages(self):
        fb_ids = []
        query = "start n=node(*) match n-[r*]->m where not(m-->())"\
                " return distinct m.fb_id"
        logger.info("using query= " + query)
        for fb_id in self.graph.cypher.execute(query):
            logger.info("Got fb_id = " + str(fb_id))
            fb_ids.append(str(fb_id))        
        return fb_ids

    def get_pages(self, limit=10):
        pages = []
        query = "MATCH (a)-[r]->(b) return b LIMIT " + str(limit)
        for page in self.graph.cypher.execute(query):
            pages.append(page[0].properties)
        return pages

