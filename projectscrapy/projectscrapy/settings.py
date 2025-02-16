BOT_NAME = "projectscrapy"

SPIDER_MODULES = ["projectscrapy.spiders"]
NEWSPIDER_MODULE = "projectscrapy.spiders"

FEED_EXPORT_INDENT = 4

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
   'projectscrapy.pipelines.CleanTextPipeline': 1,
   'projectscrapy.pipelines.PreprocessingPipeline': 2,
   'projectscrapy.pipelines.SqlitePipeline': 300,
}
# Obey robots.txt rules
ROBOTSTXT_OBEY = True

COOKIES_ENABLED = False

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


