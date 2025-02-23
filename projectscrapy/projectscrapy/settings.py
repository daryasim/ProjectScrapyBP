BOT_NAME = "projectscrapy"

SPIDER_MODULES = ["projectscrapy.spiders"]
NEWSPIDER_MODULE = "projectscrapy.spiders"

FEED_EXPORT_INDENT = 4


FEEDS = {
    "s3://projectscrapybp/%(name)s/%(name)s_%(time)s.jsonl": {
    "format": "jsonlines",
    }
}

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
   'projectscrapy.pipelines.CleanTextPipeline': 1,
   'projectscrapy.pipelines.PreprocessingPipeline': 2,
   'projectscrapy.pipelines.SqlitePipeline': 3,
}
# Obey robots.txt rules
ROBOTSTXT_OBEY = True

COOKIES_ENABLED = False

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

#scrapeops monitoring
SCRAPEOPS_API_KEY = '5b43e41b-8e60-494f-a452-12c97db6de20'

EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

