# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from reddit.items import RedditItem

class BlockchainSpider(scrapy.Spider):

    name = 'blockchain'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/BlockChain/']

    def parse(self, response):

        postings = response.xpath('//div[@class="top-matter"]')

        for record in postings:

            # Create item object to capture data
            item = RedditItem()

            item['docTitle'] = record.xpath('p[@class="title"]/a/text()').extract_first()
            docUrlBuilder = record.xpath('p[@class="title"]/a/@href').extract_first()
            item['docUrl'] = response.urljoin(docUrlBuilder)
            item['docAuthor'] = record.xpath('p[@class="tagline "]/a/text()').extract_first()
            item['docAuthorUrl'] = record.xpath('p[@class="tagline "]/a/@href').extract_first()
            item['docTimestamp'] = record.xpath('p[@class="tagline "]/time/@datetime').extract_first()[:10]
            yield item

            # Call the function to get the next page
            relative_next_url = response.xpath('//span[@class="next-button"]/a/@href').extract_first()

            # Get the URL for the next page
            absolute_next_url = response.urljoin(relative_next_url)

            # Recursively call the parse function to get content from the next page
            yield Request(absolute_next_url, callback=self.parse)
