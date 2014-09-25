# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
reload(sys)
from scrapy.exceptions import DropItem
import MySQLdb
sys.setdefaultencoding('utf-8')

from scrapy import FormRequest,Request
import scrapy

class RemoveMarkupPipeline(object):
	def __init__(self):
		pass
	def process_item(self,item,spider):
		return item

class JsonWriterPipeline(object):
	def __init__(self):
		self.file = open('news.json','wb')
	
	def process_item(self,item,spider):
		if len(item) > 0 and len(item['text']) > 0:
			line = json.dumps(dict(item),ensure_ascii = False).encode('utf-8') 
			self.file.write(line+'\n')
			return line
		else:
			raise DropItem("Missing title in %s" % item)
import time
import random
import hashlib
import urllib
import urllib2

class DataBaseWriterPipeline(object):
	def __init__(self):
		self.username = '13560323563'
		self.password = 'Liu015202'
		self.db   = 'app_cansong'
		self.host_m = 'http://w.rdc.sae.sina.com.cn'
		self.port = '3307'
	def generateSignature(self,token,timestamp,nounce):
		signature = ""
		para = [token,timestamp,nounce]
		para = sorted(para, cmp=None, key=None)
		signature = hashlib.sha1(''.join(para)).hexdigest()
		return signature
	def connectDB(self):
		conn=MySQLdb.connect(host=self.host_m + ":" + self.port,user=self.username,passwd=self.password,db=self.db,charset="utf8")  
		cursor = conn.cursor() 
		return cursor
	def process_item(self,item,spider):
		#cursor = self.connectDB()
		token = 'Cqmygcansong'
		timestamp = str(time.time())
		nonce =  str(random.random())
		signature = self.generateSignature(token,timestamp,nonce)
		url = "http://1.cansong.sinaapp.com/receivenews.php?signature=%s&timestamp=%s&nonce=%s"%(signature,timestamp,nonce)
		print "dd"
		formdata = {"jsonStr":str(item)}
		self.post(url,formdata)
		return item
	def post(self,url,data):
		f = urllib2.urlopen(url = url,data = urllib.urlencode(data))
		f.read()

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


