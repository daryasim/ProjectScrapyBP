import scrapy
from bs4 import BeautifulSoup
import re

from projectscrapy.items import MainItem


class WikipediaskSpider(scrapy.Spider):
    name = 'wikipediask'
    allowed_domains = ['sk.wikipedia.org']
    start_urls = ['https://sk.wikipedia.org']
    url_limit = 1000
    custom_settings = {
        'DEPTH_LIMIT': '10'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'url': url, 'url_count': 1})

    def parse(self, response):
        url_count = response.meta['url_count']
        if url_count >= self.url_limit:
            return
        try:
            linky = response.css('a::attr(href)').getall()
            correct_linky = [link for link in linky if
                             re.match(r'/wiki/[a-zA-Z]', link) and ':' not in link]
            if correct_linky:
                for link in correct_linky:
                    next_page_url = response.urljoin(link)
                    yield response.follow(next_page_url, callback=self.parse_article,
                                          meta={'url': response.meta['url'], 'url_count': url_count + 1},
                                          dont_filter=True)
        except Exception as e:
            self.logger.error(e)

    def parse_article(self, response):
        url_count = response.meta['url_count']
        if url_count >= self.url_limit:
            return
        try:
            soup = BeautifulSoup(response.body, 'html.parser')
            nazov = soup.select_one('h1').get_text()
            paragraphs = [p.get_text() for p in soup.select('div.mw-content-ltr.mw-parser-output p')]
            textovy_content = ' '.join(paragraphs)

            item = MainItem(
                title=nazov,
                content=textovy_content,
                url=response.url
            )
            yield item

            article_linky = response.css('a::attr(href)').getall()
            correct_article_linky = [link for link in article_linky if
                                     re.match(r'/wiki/[a-zA-Z]', link) and ':' not in link]
            for link in correct_article_linky:
                next_page_url = response.urljoin(link)
                yield response.follow(next_page_url, callback=self.parse,
                                      meta={'url': response.meta['url'], 'url_count': url_count + 1},
                                      dont_filter=True)
        except Exception as e:
            self.logger.error(e)
