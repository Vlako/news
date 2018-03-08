# -*- coding: utf-8 -*-
import scrapy


class MeduzaSpider(scrapy.Spider):
    name = 'meduza'
    allowed_domains = ['meduza.io']
    start_urls = [
        'http://meduza.io/',
        'https://meduza.io/articles',
        'https://meduza.io/razbor',
        'https://meduza.io/shapito'
    ]

    def parse(self, response):
        news = {
            'text': ''.join(response.css('div.Body *::text').extract()),
        }
        if news['text'].strip():
            yield news

        for href in response.css('a.Related--isRich::attr(href)'):
            yield response.follow(href, self.parse)

        for href in response.css('a.NewsTitle::attr(href)'):
            yield response.follow(href, self.parse)
