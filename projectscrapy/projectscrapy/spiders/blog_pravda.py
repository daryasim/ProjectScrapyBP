import scrapy
from bs4 import BeautifulSoup

from projectscrapy.items import MainItem


class BlogPravdaSpider(scrapy.Spider):
    name = "blog_pravda"
    allowed_domains = ["blog.pravda.sk"]
    start_urls = ["https://blog.pravda.sk/?page=vsetky-clanky"]
    page_limit = 10
    page_count = 0

    def parse(self, response):
        clanky_linky = response.css('div.najnovsiePrispevky.mato h2 a::attr(href)').getall()
        for link in clanky_linky:
            yield response.follow(link, callback=self.parse_article)

        if self.page_count < self.page_limit:
            next_page = response.css('a.nextpostslink::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                self.page_count += 1
                yield response.follow(next_page_url, callback=self.parse, dont_filter=True)

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
