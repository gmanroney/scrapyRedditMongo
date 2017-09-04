# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from reddit.items import RedditItem
import hashlib

class BlockchainSpider(scrapy.Spider):

    # Define spider name and URLs to process
    name = 'blockchain'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/BlockChain/']

    def parse(self, response):

        # Extract the sections about each posting
        postings = response.xpath('//div[@class="top-matter"]')

        # Loop through each entry and process
        for record in postings:

            # Create item object to capture data
            item = RedditItem()

            # Parse record using xpath to extract variables we want
            item['docTitle'] = record.xpath('p[@class="title"]/a/text()').extract_first()
            docUrlBuilder = record.xpath('p[@class="title"]/a/@href').extract_first()
            item['docUrl'] = response.urljoin(docUrlBuilder)
            item['docUrlHash'] = hashlib.sha224(item['docUrl']).hexdigest()
            item['docAuthorUrl'] = record.xpath('p[@class="tagline "]/a/@href').extract_first()

            # If author not specified use start_urls as default value
            if item['docAuthorUrl'] is None:
                item['docAuthorUrl'] = "NoAuthorGiven"

            item['docAuthorUrlHash'] = hashlib.sha224(item['docAuthorUrl']).hexdigest()
            item['docTimestamp'] = record.xpath('p[@class="tagline "]/time/@datetime').extract_first()[:10]

            # Return item
            yield item

            # Call the function to get the next page
            relative_next_url = response.xpath('//span[@class="next-button"]/a/@href').extract_first()

            # Get the URL for the next page
            absolute_next_url = response.urljoin(relative_next_url)

            # Recursively call the parse function to get content from the next page
            yield Request(absolute_next_url, callback=self.parse)
