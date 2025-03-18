import scrapy
from bs4 import BeautifulSoup

from projectscrapy.items import MainItem


class NovinySpider(scrapy.Spider):
    name = 'noviny'
    allowed_domains = ['noviny.sk']
    start_urls = [
        'https://noviny.sk',
        'https://noviny.sk/zahranicie',
        'https://noviny.sk/slovensko',
        'https://noviny.sk/krimi',
        'https://noviny.sk/politika',
    ]

    def parse(self, response):
        try:
            clanky_linky = response.css('h3.title a::attr(href)').getall()
            for link in clanky_linky:
                yield response.follow(link, callback=self.parse_article)
        except Exception as e:
            self.logger.error(e)

    def parse_article(self, response):
        try:
            soup = BeautifulSoup(response.body, 'html.parser')
            nazov = soup.select_one('h1').get_text()
            target_divs = soup.select('div.c-rte, div.entry')
            paragraphs = [p for div in target_divs for p in div.find_all('p')]
            textovy_content = ' '.join(p.get_text() for p in paragraphs)

            item = MainItem(
                title=nazov,
                content=textovy_content,
                url=response.url
            )
            yield item
        except Exception as e:
            self.logger.error(e)
