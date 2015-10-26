# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import os

class ZnxinPipeline(object):
    directory = '/downloads/data'
    
    def __init__(self):
        self.directory = '/downloads/data/zhulianwang/%s' % str(datetime.date.today())
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
    
    def process_item(self, item, spider):
        file = open((self.directory + '/%s.html') % item['name'], 'w')
        file.write(item['html'].encode('utf-8'))
        file.close()
        return item
