# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	title = scrapy.Field()
	link =  scrapy.Field()
	desc =  scrapy.Field()

class NavItem(scrapy.Item):
	title = scrapy.Field()
	link  = scrapy.Field()
	desc  = scrapy.Field()

class NewsItem(scrapy.Item):
	news_id  = scrapy.Field()
	datetime  = scrapy.Field()
	source = scrapy.Field()
	
	title  = scrapy.Field()
	summary = scrapy.Field()
	text   = scrapy.Field()
	images = scrapy.Field()
	
	url    = scrapy.Field()
	nav_type = scrapy.Field()
	keywords = scrapy.Field()
	labels = scrapy.Field()		
	
	heat_part = scrapy.Field()
	heat_comm = scrapy.Field()
