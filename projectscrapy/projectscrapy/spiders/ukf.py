import scrapy
from bs4 import BeautifulSoup

from projectscrapy.items import MainItem


class UkfSpider(scrapy.Spider):
    name = "ukf"
    allowed_domains = ["ukf.sk"]
    start_urls = ["https://www.ukf.sk/verejnost/aktuality/udalosti"]
    page_limit = 10
    page_count = 0

    def parse(self, response):
        clanky_linky = response.css('td.list-title a::attr(href)').getall()
        for link in clanky_linky:
            yield response.follow(link, callback=self.parse_article)

        if self.page_count < self.page_limit:
            next_page = response.css('li a[title="Nasl."]::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield response.follow(next_page, callback=self.parse, dont_filter=True)

    def parse_article(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        title = soup.select_one('article h1').get_text()
        target_divs = soup.select('article div')
        text_contents = []
        for div in target_divs:
            text_content = div.get_text()
            text_contents.append(text_content)
        content = " ".join(text_contents)

        item = MainItem(
            title=title,
            content=content,
            url=response.url
        )
        yield item
