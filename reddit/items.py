# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class RedditItem(Item):
    # define the fields for your item here like:
    docTitle = Field()
    docUrl = Field()
    docAuthor = Field()
    docAuthorUrl = Field()
    docTimestamp = Field()
