# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import scrapy


class VestiSpider(scrapy.Spider):
    name = 'vesti'
    allowed_domains = ['vesti.ru']
    start_urls = ['https://www.vesti.ru/news/index/']

    current_date = datetime.now()

    def parse_news(self, response):
        news = {
            'text': '\n'.join(response.css('div.js-mediator-article p::text').extract()),
        }
        if news['text'].strip():
            yield news

    def parse(self, response):

        for href in response.css('.b-item__title  a::attr(href)'):
            yield response.follow(href, self.parse_news)

        news_for_date = self.start_urls[0] + 'date/' + '.'.join([
            str(self.current_date.day).zfill(2),
            str(self.current_date.month).zfill(2),
            str(self.current_date.year)
        ])
        self.current_date -= timedelta(days=1)
        yield response.follow(news_for_date, self.parse)
