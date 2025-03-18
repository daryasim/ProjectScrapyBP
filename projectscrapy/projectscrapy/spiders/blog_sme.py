import scrapy
from bs4 import BeautifulSoup

from projectscrapy.items import MainItem


class BlogSmeSpider(scrapy.Spider):
    name = 'blog_sme'
    allowed_domains = ['blog.sme.sk']
    start_urls = ['https://blog.sme.sk/']
    page_limit = 5
    page_count = 0

    def parse(self, response):
        try:
            clanky_linky = response.css('a.title::attr(href)').getall()
            for link in clanky_linky:
                yield response.follow(link, callback=self.parse_article)

            if self.page_count < self.page_limit:
                next_page = response.css('a.btn.btn-border.icon-right.align-right::attr(href)').get()
                if next_page:
                    next_page_url = response.urljoin(next_page)
                    self.page_count += 1
                    yield response.follow(next_page_url, callback=self.parse, dont_filter=True)
        except Exception as e:
            self.logger.error(e)

    def parse_article(self, response):
        try:
            soup = BeautifulSoup(response.body, 'html.parser')
            nazov = soup.select_one('h1').get_text()
            paragraphs = [p.get_text() for p in soup.select('div.article-body-content')]
            textovy_content = ' '.join(paragraphs)

            item = MainItem(
                title=nazov,
                content=textovy_content,
                url=response.url
            )
            yield item
        except Exception as e:
            self.logger.error(e)
