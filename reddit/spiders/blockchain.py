# -*- coding: utf-8 -*-
import scrapy


class BlockchainSpider(scrapy.Spider):
    name = 'blockchain'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/BlockChain//']

    def parse(self, response):
        pass
