# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import scrapy


class LentaSpider(scrapy.Spider):
    name = 'lenta'
    allowed_domains = ['lenta.ru']
    current_date = datetime.now()
    start_urls = ['https://lenta.ru']

    def parse_news(self, response):
        news = {
            'text': '\n'.join(response.css('div.b-text p::text').extract()),
        }
        if news['text'].strip():
            yield news

    def parse(self, response):

        for href in response.css('.titles h3 a::attr(href)'):
            yield response.follow(href, self.parse_news)

        news_for_date = '/'.join([
            self.start_urls[0],
            str(self.current_date.year),
            str(self.current_date.month).zfill(2),
            str(self.current_date.day).zfill(2)
        ])
        self.current_date -= timedelta(days=1)
        yield response.follow(news_for_date, self.parse)
