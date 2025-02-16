from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from projectscrapy.spiders.noviny import NovinySpider
from projectscrapy.spiders.ukf import UkfSpider
from projectscrapy.spiders.blog_sme import BlogSmeSpider
from projectscrapy.spiders.blog_pravda import BlogPravdaSpider
from projectscrapy.spiders.vedanadosah import VedanadosahSpider
from projectscrapy.spiders.wikipediask import WikipediaskSpider

process = CrawlerProcess(get_project_settings())

process.crawl(NovinySpider)
process.crawl(UkfSpider)
process.crawl(BlogSmeSpider)
process.crawl(BlogPravdaSpider)
process.crawl(VedanadosahSpider)
process.crawl(WikipediaskSpider)

process.start()
