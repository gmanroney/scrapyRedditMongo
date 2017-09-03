# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class BlockchainSpider(scrapy.Spider):
    name = 'blockchain'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/BlockChain/']

    def parse(self, response):

        postings = response.xpath('//p[@class="title"]')

        for record in postings:
            docTitle = record.xpath('a/text()').extract_first()
            docUrl = record.xpath('a/@href').extract_first()
            docUrl = response.urljoin(docUrl)
            yield { 'Title': docTitle, 'URL': docUrl }
            relative_next_url = response.xpath('//a[@class="next-button"]/@href').extract_first()
            absolute_next_url = response.urljoin(relative_next_url)
            yield Request(absolute_next_url, callback=self.parse)
