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
