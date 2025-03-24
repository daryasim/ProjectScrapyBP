import scrapy
from bs4 import BeautifulSoup

from projectscrapy.items import MainItem


class UkfSpider(scrapy.Spider):
    name = 'ukf'
    allowed_domains = ['ukf.sk']
    start_urls = ['https://www.ukf.sk/verejnost/aktuality/udalosti']
    page_limit = 5

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'url': url, 'page_count': 1})

    def parse(self, response):
        page_count = response.meta['page_count']
        article_linky = response.css('td.list-title a::attr(href)').getall()
        for link in article_linky:
            yield response.follow(link, callback=self.parse_article)

        if page_count < self.page_limit:
            next_page = response.css('li a[title="Nasl."]::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield response.follow(next_page_url, callback=self.parse,
                                      meta={'url': response.meta['url'], 'page_count': page_count + 1},
                                      dont_filter=True)

    def parse_article(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        title = soup.select_one('article h1').get_text()
        target_divs = soup.select('article div')
        content = ' '.join(div.get_text() for div in target_divs)

        item = MainItem(
            title=title,
            content=content,
            url=response.url
        )
        yield item
