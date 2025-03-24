import scrapy
from bs4 import BeautifulSoup

from projectscrapy.items import MainItem


class BlogPravdaSpider(scrapy.Spider):
    name = 'blog_pravda'
    allowed_domains = ['blog.pravda.sk']
    start_urls = ['https://blog.pravda.sk/vsetky-clanky/']
    page_limit = 5

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'url': url, 'page_count': 1})

    def parse(self, response):
        page_count = response.meta['page_count']
        article_linky = response.css('div.najnovsiePrispevky.mato h2 a::attr(href)').getall()
        for link in article_linky:
            yield response.follow(link, callback=self.parse_article)
        if page_count < self.page_limit:
            next_page = response.css('a.nextpostslink::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield response.follow(next_page_url, callback=self.parse,
                                      meta={'url': response.meta['url'], 'page_count': page_count + 1},
                                      dont_filter=True)

    def parse_article(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        nazov = soup.select_one('div.post-title h2').get_text()
        paragraphs = [p.get_text() for p in soup.select('div[itemprop="articleBody"] p')]
        textovy_content = ' '.join(paragraphs)

        item = MainItem(
            title=nazov,
            content=textovy_content,
            url=response.url
        )
        yield item

