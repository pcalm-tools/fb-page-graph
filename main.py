from crawler import Crawler
import logging
import os
import yaml

#os.environ['http_proxy']=''
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
config   = yaml.load(file('config.yaml', 'r'))
crawler = Crawler(config)
crawler.recursive_crawling()