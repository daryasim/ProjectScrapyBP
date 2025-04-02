import scrapy
import json
import os

from projectscrapy.items import MainItem

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_file = os.path.join(base_dir, 'websites.json')
with open(input_file, 'r', encoding='utf-8') as file:
    json_settings = json.load(file)


class GeneralSpiderSpider(scrapy.Spider):
    name = 'generalspider'

    def start_requests(self):
        for json_setting in json_settings['websites']:
            for url in json_setting['start_urls']:
                yield scrapy.Request(url=url, callback=self.parse, meta={'web_data': json_setting})

    def parse(self, response):
        json_setting = response.meta['web_data']
        article_linky = []
        for selector in json_setting.get('link_selector', []):
            article_linky.extend(response.xpath(selector).getall())
        for link in article_linky:
            yield response.follow(link, callback=self.parse_article, meta={'web_data': json_setting})
        if json_setting.get('pagination_link'):
            actual_page = response.meta.get('actual_page', 1)
            yield from self.pagination(response, json_setting, actual_page)

    def pagination(self, response, json_setting, actual_page):
        page_limit = json_setting.get('page_limit', float('inf'))
        if actual_page >= page_limit:
            return
        next_page = response.xpath(json_setting['pagination_link']).get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(
                next_page_url,
                callback=self.parse,
                meta={'web_data': json_setting, 'actual_page': actual_page + 1},
                dont_filter=True
            )
        else:
            self.logger.info('No link, check selector')

    def parse_article(self, response):
        json_setting = response.meta['web_data']
        nazov = response.xpath(json_setting['title_selector']).get()
        if not nazov:
            self.logger.warning(f'No title, check selector')
        content = []
        for selector in json_setting['content_selectors']:
            content.extend(response.xpath(selector).getall())
        if not content:
            self.logger.warning(f'No content, check selector')
        textovy_content = ' '.join(content)

        item = MainItem(
            title=nazov,
            content=textovy_content,
            url=response.url
        )
        yield item
        

