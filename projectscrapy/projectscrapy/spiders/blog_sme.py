import scrapy
from bs4 import BeautifulSoup

from projectscrapy.items import MainItem


class BlogSmeSpider(scrapy.Spider):
    name = 'blog_sme'
    allowed_domains = ['blog.sme.sk']
    start_urls = ['https://blog.sme.sk/']
    page_limit = 5

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'url': url, 'page_count': 1})

    def parse(self, response):
        page_count = response.meta['page_count']
        try:
            article_linky = response.css('a.title::attr(href)').getall()
            for link in article_linky:
                yield response.follow(link, callback=self.parse_article)

            if page_count < self.page_limit:
                next_page = response.css('a.btn.btn-border.icon-right.align-right::attr(href)').get()
                if next_page:
                    next_page_url = response.urljoin(next_page)
                    yield response.follow(next_page_url, callback=self.parse,
                                          meta={'url': response.meta['url'], 'page_count': page_count + 1},
                                          dont_filter=True)
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
