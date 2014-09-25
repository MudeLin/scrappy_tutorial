import scrapy

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
	name = "dmoz"
	allow_domains = ["dmoz.org"]
	start_urls = [
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
	]
	def parse(self,response):
		items = []
		for sel in response.xpath('//ul[@class="directory-url"]/li'):
			item = DmozItem() 
			item['title'] = sel.xpath('a/text()').extract()
			item['link'] = sel.xpath('a/@href').extract()
			item['desc'] = sel.xpath('text()').re('-\s([^\n]*?)\\n')
			items.append(item)
#		return items
