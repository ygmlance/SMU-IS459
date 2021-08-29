# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class HardwarezonePipeline:
    def process_item(self, item, spider):
        return item

class RemoveWhiteSpacePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if "content" in adapter:
            content = adapter["content"]
            new_content = []
            
            for string in content:
                string = string.replace("\n", " ")
                string = string.replace("\t", " ")
                string = string.strip()
                
                if string.startswith("{") and string.endswith("}"):
                    string = ""
                
                new_content.append(string)
                
            new_content = list(filter(("").__ne__, new_content))
            adapter["content"] = " ".join(new_content).strip()
        
        return item


class MongoDbPipeline:
    
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection = mongo_collection
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGODB_SERVER'),
            mongo_db = crawler.settings.get('MONGODB_DB'),
            mongo_collection = crawler.settings.get('COLLECTION')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        
    def close_spider(self, spider):
        self.client.close()
        
    def process_item(self, item, spider):
        self.db[self.collection].insert_one(ItemAdapter(item).asdict())
        return item
    
    pass