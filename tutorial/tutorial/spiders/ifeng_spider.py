#coding=utf-8
import scrapy
from scrapy import Request
from tutorial.items import NewsItem
import datetime as dt
import re
class iFengSpider(scrapy.Spider):
	name="ifeng"
	allow_domains = ["ifeng.com"]
	start_urls = ["http://www.ifeng.com"]
	
	def parse(self, response):
		
		blocks = response.xpath('//div[@class="col"]/div[@class="col_R"]/div[@class="block"]')
		flag = False
		#print "blocks",len(blocks)
		nav_titles = []
		item_urls = []
		for block in blocks:
			left_boxs = block.xpath('.//div[@class="box360"]')
			right_boxs = []
			#print 'left boxes',len(left_boxs)
			if flag != False:
				right_boxs = block.xpath('.//div[@class="box360 p_30"]')
				#print 'right boxes',len(right_boxs)
				boxes = left_boxs + right_boxs
				for box in boxes:
					nav_title = box.xpath('.//div[@class="tit02"]/span[@class="ch"]/a/text()').extract()
					if len(nav_title) > 0:
						nav_title = str(nav_title[0])
					else:
						print "Error: cannot find nav "
						continue
					items = box.xpath('.//div[@class="picTxt"] |.//ul[@class="list01"]')	
					items = items.xpath('.//a')
					#print nav_title
					for item in items:
						try:
							link = item.xpath('./@href').extract()[0]
							title = item.xpath('./text()').extract()[0]
						#print title,link
							request =  Request(url = link, callback=self.parse_item)
							request.meta['nav_type'] = nav_title
							yield request
						except:
							print "Got an empty title link"
			else:
				flag = True
				for box in left_boxs:
					nav_title = box.xpath('.//div[@class="clearfix"]//a/text()').extract()
					if len(nav_title) > 0:
						nav_title = str(nav_title[0])
					else:
						nav_title = "要闻"
					nav_titles.append(nav_title)
					headlines = box.xpath('.//div[@id="headLineDefault"]//a')
					for item in headlines:
						link = item.xpath('./@href').extract()[0]
						title = item.xpath('./text()').extract()[0]
						request = Request(url = link, callback=self.parse_item)
						request.meta['nav_type'] = nav_title
						yield request
	def parse_item(self,response):
		article = response.xpath('//div[@id="artical"]')
		news = NewsItem()
		for art in article:
			news['title'] = str(art.xpath('.//h1[@id="artical_topic"]/text()').extract()[0])
			print news['title']
			art_sth = art.xpath('./div[@id="artical_sth"]')
			datetimePa = "\d{4}.\d{1,2}.\d{1,2}. \d{1,2}:\d{1,2}"
			try:
				news['datetime'] = art_sth.xpath('.//*/text()').re(datetimePa)[0];
			except:
				now = dt.datetime.now()
				news['datetime'] = now.strftime( '%Y年%m月%d日 %H:%M:%S' )
			try:
				news['source'] =  art_sth.xpath('./p/span[@itemprop="publisher"]//a/text()').extract()[0] 
			except:
				try:
					sourcePa = re.compile('来源：.*?( |\n|$|<)?',re.DOTALL)
					text = art_sth.xpath('.//*/text()').extract()
					sources = sourcePa.findall(text)
					news['source'] = sources[0][4:]
				except:
					news['source'] = 'ifeng.com'
					
			try:
				news['heat_part'] = art_sth.xpath('./div/h5/span/a/em/text()').extract()[0]
				news['heat_comm'] = art_sth.xpath('./div/h5/a/em/text()').extract()[0]
			except:
				print "JS require"
				news['heat_part'] = 0
				news['heat_comm'] = 0
			art_real = art.xpath('./div[@id="artical_real"]')
			try:
				news['summary'] = art_real.xpath('./div[@class="dy_box ss_none"]/p/text()').extract()[0]
			except:
				news['summary'] = ''
				print "Empty summary"
			art_main = art_real.xpath('./div[@id="main_content"]')
			
			news['images'] = "|".join(art_main.xpath('./p[@class="detailPic"]/img/@src').extract())
			
			news['text'] = "\n".join(art_main.xpath('./p/text()').extract())
			
			art_sth2 = art.xpath('./div[@id="artical_sth2"]')

			news['labels'] = "|".join(art_sth2.xpath('./p[@class="p01 ss_none"]/a/text()').extract())
			news['nav_type'] = response.meta['nav_type']
			news['url']  = response.url
			news['keywords'] = ""
		return news
