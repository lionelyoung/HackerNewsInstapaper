# Scrapy settings for scrapyhacker project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'scrapyhacker'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['scrapyhacker.spiders']
NEWSPIDER_MODULE = 'scrapyhacker.spiders'
DEFAULT_ITEM_CLASS = 'scrapyhacker.items.ScrapyhackerItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES =['scrapyhacker.pipelines.FilterEmptyPipeline',
                 'scrapyhacker.pipelines.scrapeDatasqLitePipeline',
                ]
