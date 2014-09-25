#coding=utf-8
import scrapy
from scrapy import Request
class BiduSpider(scrapy.Spider):
	name = "baidu"
	allow_domains = ["baidu.com"]
	start_urls = ["http://news.baidu.com"]
	
	def parse(self,response):
		navs = response.xpath('//div[@class="menu-list"]/ul/li')
		nav_urls = []
		for nav in navs:
			title = nav.xpath("a/text()").extract()[0]
			link = nav.xpath("a/@href").extract()[0]
			nav_urls.append(link)
		#	print title.encode('utf-8'),link
	    	
		for nav_url in nav_urls:
			print nav_url
			yield Request(url=nav_url,callback=self.parse_nav)
		
	def parse_nav(self,response):
		items = response.xpath('//div[@class="hotnews"]/ul/li/strong')
		item_urls = []
		for item in items:
			title = item.xpath("a/text()").extract()[0]
			link  = item.xpath("a/@href").extract()[0]
			item_urls.append(link)

		for item_url in item_urls:
			print item_url
			yield Request(url = item_url,callback = self.parse_item)

	def parse_item(self,response):
		pass
	def parse_detail(self,response):
		pass
