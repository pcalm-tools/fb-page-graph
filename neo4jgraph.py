from py2neo import Graph, Node, Relationship, watch, schema, error
import pprint
import logging

class N4JGraphController:
    graph = None
    def __init__(self, config):
        self.graph = Graph(config['url'])
        self.initialize_schema()

    #TODO: Check if schema is not already created
    def initialize_schema(self):
        try:
            self.graph.schema.create_uniqueness_constraint('Page', 'fb_id')
            self.graph.schema.create_uniqueness_constraint('Page', 'username')
        except Exception as e:
            logging.info('Skipping creation of unique constraint')
            
    def add(self, page):        
        page = self.fix_format(page)
        node = self.graph.merge_one('Page', 'fb_id', page['fb_id'])
        node.properties.update(page)
        node.push()
        return node

    def add_relation(self, page1, relation, page2):
        self.graph.create_unique(Relationship(page1, relation, page2))

    def delete_all(self):
        logging.warn('Deleting all nodes')
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

    #FIXME: Query is not correct
    def get_leaf_pages(self):
        pages = []
        query = "MATCH (a)-[r]->(b) return b.fb_id as fb_id";
        for page in self.graph.cypher.execute(query):
            pages.append(str(page.fb_id))
        return pages

    def get_pages(self, limit=10):
        pages = []
        query = "MATCH (a)-[r]->(b) return b LIMIT " + str(limit)
        for page in self.graph.cypher.execute(query):
#            pages.append(str(page.fb_id))
            pages.append(page[0].properties)

            #logging.info(pprint.pformat(page))
            logging.info(type(page))
            logging.info(pprint.pformat(page[0].properties))

        return pages

