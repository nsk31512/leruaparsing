# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeruaparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase =client.leroy_products

    def process_item(self, item, spider):
        item['name'] = item['name'][0]
        item['url'] = item['url'][0]
        item['price'] = float(item['price'][0])
        item['_id'] = int(item['_id'][0])

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item


class LeruaparserPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print()
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, result, item, info):
        item['photos'] = [itm[1] for itm in result if itm[0]]
        return item

