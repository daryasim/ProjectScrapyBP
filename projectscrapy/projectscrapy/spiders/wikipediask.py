import scrapy
from bs4 import BeautifulSoup
import re

from projectscrapy.items import MainItem


class WikipediaskSpider(scrapy.Spider):
    name = "wikipediask"
    allowed_domains = ["sk.wikipedia.org"]
    start_urls = ["https://sk.wikipedia.org"]
    url_limit = 100
    url_count = 0
    custom_settings = {
        "DEPTH_LIMIT": 5
    }

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return

        links = response.css('a::attr(href)').getall()
        correct_links = [link for link in links if re.match(r'/wiki/[a-zA-Z]', link) and ':' not in link]

        if correct_links:
            for link in correct_links:
                next_page_url = response.urljoin(link)
                self.url_count += 1
                yield response.follow(next_page_url, callback=self.parse_article)

    def parse_article(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        nazov = soup.select_one('h1.firstHeading span').get_text()
        paragraphs = [p.get_text() for p in soup.select('div.mw-content-ltr.mw-parser-output p')]
        textovy_content = ' '.join(paragraphs)

        item = MainItem(
            title=nazov,
            content=textovy_content,
            url=response.url
        )
        yield item

        if self.url_count < self.url_limit:
            links_article = response.css('a::attr(href)').getall()
            correct_links_article = [link for link in links_article if re.match(r'/wiki/[a-zA-Z]', link) and ':' not in link]
            for link in correct_links_article:
                next_page_url = response.urljoin(link)
                self.url_count += 1
                if self.url_count <= self.url_limit:
                    yield response.follow(next_page_url, callback=self.parse_article)


