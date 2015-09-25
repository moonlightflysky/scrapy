# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

class DpdemoPipeline(object):

    """def __init__(self):
        self.file = codecs.open('test_data_utf8.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        # print line
        self.file.write(line.decode("unicode_escape"))
        return item"""

    def __init__(self):
        self.file = open('results.txt',mode='wb')

    def process_item(self, item, spider):
        self.file.write(item['name'].encode("utf-8"))
        self.file.write("\n")

        self.file.write(item['stars'].encode("utf-8"))
        self.file.write("\n")

        self.file.write(item['binfo'].encode("utf-8"))
        self.file.write("\n")

        self.file.write('时间 ： ')
        self.file.write(item['time'].encode("utf-8"))
        self.file.write("\n")


        self.file.write('标签 ： ')
        self.file.write(item['labels'].encode("utf-8"))
        self.file.write("\n")

        return item
