# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from peewee import *
db = SqliteDatabase('zoro.db')

class Product(Model):
    category = CharField(null=True)
    brand = CharField(null=True)
    title = CharField(null=True)
    zoro_id = CharField(null=True)
    mfr_no = CharField(null=True)
    price = CharField(null=True)
    description = CharField(null=True)
    
    class Meta:
        database = db
        table_name = "products"

class ZoroPipeline:
    def open_spider(self, spider):
        global db
        db.connect()
        db.create_tables([Product])
        self.count = 0

    def process_item(self, item, spider):
        Product.create(**item)
        print(self.count)
        self.count += 1
        return item
        
    def close_spider(self, spider):
        db.close()


