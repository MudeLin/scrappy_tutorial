import scrapy
from scrapy import Request

class NetnewsSpider(scrapy.Spider):
	name = "netease"
	allow_domains = ["163.com"]
	start_urls = ["http://news.163.com"]

	def parse(self, response):
		nav_blues = response.xpath('//div[@class="N-nav-channel JS_NTES_LOG_FE"]/a')
		nav_urls = []
		for nav in nav_blues:
			title = nav.xpath("./text()").extract()[0].encode('utf-8')
			link  = nav.xpath("./@href").extract()[0]
			nav_urls.append(link)
		#	print title,link
		for nav_url in nav_urls:
			yield Request(url = nav_url, callback = self.parse_nav)
	
	def parse_nav(self,response):
		pass		
	
	def parse_item(self,response):
		pass
