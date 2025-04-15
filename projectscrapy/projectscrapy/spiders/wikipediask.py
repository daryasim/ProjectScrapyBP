import scrapy
from bs4 import BeautifulSoup
import re

from projectscrapy.items import MainItem


class WikipediaskSpider(scrapy.Spider):
    name = 'wikipediask'
    allowed_domains = ['sk.wikipedia.org']
    start_urls = ['https://sk.wikipedia.org']
    url_limit = 1000
    url_count = set()

    def parse(self, response):
        if len(self.url_count) >= self.url_limit:
            return
        links = response.css('a::attr(href)').getall()
        correct_linky = [link for link in links if
                         re.match(r'/wiki/[a-zA-Z]', link) and ':' not in link]
        for link in correct_linky:
            next_page_url = response.urljoin(link)
            if next_page_url not in self.url_count:
                self.url_count.add(next_page_url)
                if len(self.url_count) > self.url_limit:
                    break
                yield response.follow(next_page_url, callback=self.parse_article)

    def parse_article(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        nazov = soup.select_one('h1').get_text()
        paragraphs = [p.get_text() for p in soup.select('div.mw-body-content p')]
        textovy_content = ' '.join(paragraphs)

        item = MainItem(
            title=nazov,
            content=textovy_content,
            url=response.url
        )
        yield item

        if len(self.url_count) >= self.url_limit:
            return
        linky_article = response.css('a::attr(href)').getall()
        correct_linky_article = [link for link in linky_article if
                                 re.match(r'/wiki/[a-zA-Z]', link) and ':' not in link]
        for link in correct_linky_article:
            next_page_url = response.urljoin(link)
            if next_page_url not in self.url_count:
                self.url_count.add(next_page_url)
                if len(self.url_count) > self.url_limit:
                    break
                yield response.follow(next_page_url, callback=self.parse_article)