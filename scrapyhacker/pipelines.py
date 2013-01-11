from scrapy.exceptions import DropItem
# Author: Jay Vaughan
from scrapy import log
from pysqlite2 import dbapi2 as sqlite

class FilterEmptyPipeline(object):
    """A pipeline for filtering out empty items or non-interesting links"""

    def process_item(self, item, spider):
        if not item['link'] or 'http' not in item['link'][0]:
            raise DropItem("Invalid link")
        return item

#
# Author: Jay Vaughan
#
# Pipelines for processing items returned from a scrape.
# Dont forget to add pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
#

# This pipeline takes the Item and stuffs it into scrapedata.db
class scrapeDatasqLitePipeline(object):
    def __init__(self):
        # Possible we should be doing this in spider_open instead, but okay
        self.connection = sqlite.connect('./articles.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, link VARCHAR(200), title VARCHAR(200), num_comments INTEGER, submitted BOOLEAN)')

    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        self.cursor.execute("select * from articles where link=?", item['link'])
        result = self.cursor.fetchone()
        if result:
            log.msg("Item already in database: %s" % item, level=log.DEBUG)
            raise DropItem("Duplicate in database")
        else:
            self.cursor.execute(
                "insert into articles (link, title, num_comments, submitted) values (?, ?, ?, ?)",
                    (item['link'][0], item['title'][0], item['num_comments'], '0'))
            self.connection.commit()

        log.msg("Item stored: %s" % item['link'][0], level=log.DEBUG)
        return item

    def handle_error(self, e):
        log.err(e)
