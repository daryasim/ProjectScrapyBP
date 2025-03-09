import scrapy
from bs4 import BeautifulSoup

from projectscrapy.items import MainItem

class VedanadosahSpider(scrapy.Spider):
    name = 'vedanadosah'
    allowed_domains = ['vedanadosah.cvtisr.sk']
    start_urls = [
        'https://vedanadosah.cvtisr.sk/vsetky-clanky/'
    ]
    page_limit = 5
    page_count = 0

    def parse(self, response):
        clanky_linky = response.css('div.col-md-8 h4 a::attr(href)').getall()
        for link in clanky_linky:
            yield response.follow(link, callback=self.parse_article)

        if self.page_count < self.page_limit:
            next_page = response.css('a.next.page-numbers::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                self.page_count += 1
                yield response.follow(next_page_url, callback=self.parse, dont_filter=True)
    def parse_article(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        nazov = soup.select_one('h1.titulok-post').get_text()
        paragraphs = [p.get_text() for p in soup.select('div.entry p')]
        textovy_content = ' '.join(paragraphs)

        item = MainItem(
            title=nazov,
            content=textovy_content,
            url=response.url
        )
        yield item
