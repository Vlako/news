# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import scrapy


class RiaSpider(scrapy.Spider):
    name = 'ria'
    allowed_domains = ['ria.ru']
    start_urls = ['http://ria.ru/archive/']
    current_date = datetime.now()

    def parse_news(self, response):
        news = {
            'text': '\n'.join(response.css('div.b-article__body::text,div.b-article__body p::text').extract()),
        }
        if news['text'].strip():
            yield news

    def parse(self, response):

        for href in response.css('.b-list__item  a::attr(href)'):
            yield response.follow(href, self.parse_news)

        news_for_date = self.start_urls[0] + ''.join([
            str(self.current_date.year),
            str(self.current_date.month).zfill(2),
            str(self.current_date.day).zfill(2)
        ])
        self.current_date -= timedelta(days=1)
        yield response.follow(news_for_date, self.parse)
