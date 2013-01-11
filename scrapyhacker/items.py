# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ScrapyhackerItem(Item):
    # define the fields for your item here like:
    title = Field()
    link = Field()
    num_comments = Field()
