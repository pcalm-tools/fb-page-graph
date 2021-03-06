from crawler import Crawler
import logging
import os
import yaml

#logging.basicConfig(format='%(levelname)s:%(message)s', 
#                    level=logging.INFO)

logging.basicConfig()
config   = yaml.load(file('resources/config.yaml', 'r'))
crawler = Crawler(config)
crawler.crawl()
