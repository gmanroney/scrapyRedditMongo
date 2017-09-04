# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
#from reddit.items import RedditItem

class BlockchainSpider(scrapy.Spider):

    name = 'blockchain'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/BlockChain/']

    def parse(self, response):

        postings = response.xpath('//div[@class="top-matter"]')

        for record in postings:

            # Create item object to capture data
            #item = RedditItem()

            docTitle = record.xpath('p[@class="title"]/a/text()').extract_first()
            docUrl = record.xpath('p[@class="title"]/a/@href').extract_first()
            docUrl = response.urljoin(docUrl)
            docAuthor = record.xpath('p[@class="tagline "]/a/text()').extract_first()
            docAuthorUrl = record.xpath('p[@class="tagline "]/a/@href').extract_first()
            docTimestamp = record.xpath('p[@class="tagline "]/time/@datetime').extract_first()[:10]
            yield { 'Title': docTitle, 'URL': docUrl, 'Author': docAuthor, 'AuthorURL': docAuthorUrl, 'DateCreated': docTimestamp }

            # Call the function to get the next page
            relative_next_url = response.xpath('//span[@class="next-button"]/a/@href').extract_first()

            # Get the URL for the next page
            absolute_next_url = response.urljoin(relative_next_url)

            # Recursively call the parse function to get content from the next page
            yield Request(absolute_next_url, callback=self.parse)

~                                                                                                                                                      
~
