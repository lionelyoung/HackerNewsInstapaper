#!/usr/bin/env python
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapyhacker.items import ScrapyhackerItem

class HackerNewsSpider(BaseSpider):
    name = "hackernews"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ['http://news.ycombinator.com/best']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        hxslinks = hxs.select('//td[@class="title"]')
        hxscomments = hxs.select('//td[@class="subtext"]/a[2]/text()')

        # Clean comments
        clean_comment = lambda x: int(x.strip('s').strip(' comment'))
        comments = [clean_comment(comment.extract()) for comment in hxscomments]

        items = []
        idx_comment = 0
        for link in hxslinks:
            item = ScrapyhackerItem()
            item['title'] = link.select('a/text()').extract()
            item['link'] = link.select('a/@href').extract()

            if item['link']:
                print idx_comment, item['link']
                try:
                    item['num_comments'] = comments[idx_comment]
                except IndexError:
                    pass
                idx_comment = idx_comment + 1

            items.append(item)
        return items
