from scrapy.item import Item, Field


class MainItem(Item):
    title = Field()
    content = Field()
    preprocessed_content = Field()
    url = Field()
