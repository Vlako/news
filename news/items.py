# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class NewsItem(Item):
    text = Field()
