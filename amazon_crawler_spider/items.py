# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonCrawlerSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    item_id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    in_stock = scrapy.Field()
    shipping_price = scrapy.Field()
    shipping_time = scrapy.Field()
    offer_listing = scrapy.Field()
