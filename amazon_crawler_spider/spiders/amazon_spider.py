import os
import re
import logging
import datetime


import scrapy
from scrapy.crawler import CrawlerProcess
from scraper_api import ScraperAPIClient
from scrapy.settings import Settings


from amazon_crawler_spider.items import AmazonCrawlerSpiderItem
from amazon_crawler_spider import settings as my_settings

client = ScraperAPIClient(my_settings.API_KEY)
logging.getLogger("scrapy").propagate = False


def process_start_urls(input_str: str):

    if os.path.isfile(os.path.normpath(input_str)):
        with open(os.path.normpath(input_str), "r") as file:
            start_url = []
            for row in file:
                row = row.strip("\n")
                start_url.append(f"https://www.amazon.com/dp/{row}")

    elif len(input_str.split(",")) == 1:
        start_url = [f"https://www.amazon.com/dp/{input_str}"]

    else:
        start_url = [
            f"https://www.amazon.com/dp/{item.strip()}" for item in input_str.split(",")
        ]

    return start_url


class AmazonSpider(scrapy.Spider):
    name = "amazon_spider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.114 Safari/537.36"
    }

    def start_requests(self):
        item_ids = input(
            "Enter product id, full path of a file or product ids seperated by ',' : "
        )
        urls = process_start_urls(item_ids.strip())
        # urls = [
        #     "https://www.amazon.com/dp/B08KYNL6LH?psc=1",
        #     # "https://www.amazon.com/dp/B07Y91V9BK?psc=1",
        # ]

        for url in urls:
            # yield scrapy.Request(client.scrapyGet(url=url,country_code='us'),callback=self.parse)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )

    def parse(self, response, **kwargs):
        item = AmazonCrawlerSpiderItem()
        item["item_id"] = self.get_item_id(response)
        item["title"] = self.get_title(response)
        item["description"] = self.get_description(response)
        item["price"] = self.get_price(response)
        item["in_stock"] = self.get_in_stock_status(response)
        item["shipping_price"] = self.get_shipping_price(response)
        item["shipping_time"] = self.get_shipping_time(response)
        offer_page = self.get_offer_page(self.get_item_id(response))
        # yield scrapy.Request(client.scrapyGet(url=offer_page,country_code='us'), callback=self.page_parse)
        yield scrapy.Request(
            url=offer_page,
            callback=self.page_parse,
            meta={"item": item},
        )

    def page_parse(self, response):
        item = response.meta.get("item")
        conditions = self.get_offers_conditions(response)
        prices = self.get_offers_prices(response)
        shipping_prices = self.get_offers_shipping_prices(response)
        shipping_time = self.get_offers_shipping_time(response)
        positive_ratings_feedbacks = self.get_offers_ratings_feedbacks(response)
        offers = list()
        for offer in zip(
            conditions,
            prices,
            shipping_prices,
            shipping_time,
            positive_ratings_feedbacks,
        ):
            temp_dict = dict()
            temp_dict["condition"] = offer[0]
            temp_dict["price"] = self.price_analise(offer[1])
            temp_dict["shipping_price"] = offer[2]
            temp_dict["shipping_time"] = offer[-2]
            temp_dict["total_rating"] = offer[-1][0]
            temp_dict["positive_feedback"] = offer[-1][1]
            offers.append(temp_dict)

        item["offer_listing"] = offers
        yield item

    def get_title(self, response):
        return self.clean(response.xpath('//*[@id="productTitle"]/text()').extract()[0])

    def get_description(self, response):
        return self.clean(
            ";".join(
                response.xpath(
                    '//*[@id="feature-bullets"]/ul/li/span/text()'
                ).extract()[2:]
            )
        )

    def get_price(self, response):
        return self.price_analise(
            self.clean(
                response.xpath(
                    '//*[@id="price_inside_buybox"]/text() | //*[@id="price"]/text()'
                ).extract()[0]
            )
        )

    def get_in_stock_status(self, response):
        return self.status_analise(
            self.clean(
                response.xpath('//*[@id="availability"]/span/text()').extract()[0]
            )
        )

    def get_shipping_price(self, response):
        return self.price_analise(
            self.clean(
                response.xpath(
                    '//*[@id="mir-layout-DELIVERY_BLOCK-slot-DELIVERY_MESSAGE"]/a[1]/text() |'
                    ' //*[@id="mir-layout-DELIVERY_BLOCK-slot-DELIVERY_MESSAGE"]/span/a/text()'
                ).extract()[0]
            )
        )

    def get_shipping_time(self, response):
        return self.time_calculator(
            self.clean(
                response.xpath(
                    '//*[@id="mir-layout-DELIVERY_BLOCK-slot-DELIVERY_MESSAGE"]/b/text()'
                ).extract()[0]
            )
        )

    @staticmethod
    def get_item_id(response):
        return response.xpath('//*[@id="ASIN"]/@value').get()

    @staticmethod
    def get_offer_page(item_id):
        return (
            f"https://www.amazon.com/gp/aod/ajax/ref=auto_load_aod?asin={item_id}&pc=dp"
        )

    def get_offers_conditions(self, response):
        return [
            self.clean(condition)
            for condition in response.xpath(
                '//*[@id="aod-offer-heading"]/h5/text()'
            ).extract()[1:]
        ]

    def get_offers_prices(self, response):
        return [
            self.clean(price)
            for price in response.css("span.a-price span.a-offscreen::text").extract()[
                1:
            ]
        ]

    def get_offers_shipping_prices(self, response):
        return [
            self.price_analise(self.clean(shipping_price.strip()))
            for shipping_price in response.xpath(
                '//*[@id="delivery-message"]/span/a[1]/text() | //*[@id="delivery-message"]/a/text() |'
                ' //*[@id="delivery-message"]/text()'
            ).extract()[2:]
            if self.clean(shipping_price).lower().__contains__("delivery")
        ]

    def get_offers_shipping_time(self, response):
        return [
            self.time_calculator(self.clean(shipping_time.strip()))
            for shipping_time in response.xpath(
                '//*[@id="delivery-message"]/b/text()'
            ).extract()[1:]
        ]

    def get_offers_ratings_feedbacks(self, response):
        positive_feedback_list = list()

        see_more = response.xpath('//*[@id="aod-offer-soldBy"]')
        see_more = (
            see_more[0].css("span.a-size-small.a-color-base span::text").extract()
        )
        if see_more:
            positive_feedback_list.append(see_more)
        else:
            positive_feedback_list.append(["None", "None"])

        positive_feedback = response.xpath('//*[@id="aod-offer"]')
        for item in positive_feedback:
            try:
                section = item.css("span.a-size-small.a-color-base")[1]
                data = section.css(
                    "span.a-size-small.a-color-base span::text"
                ).extract()
                if len(data) == 1:
                    positive_feedback_list.append(["None", "None"])
                else:
                    positive_feedback_list.append(data)
            except Exception:
                positive_feedback_list.append(["None", "None"])
                continue

        return self.clean_ratings_feedbacks(positive_feedback_list)

    @staticmethod
    def clean(extracted_data: str):
        return re.sub(r"\n\s*\n", "", extracted_data)

    @staticmethod
    def price_analise(shipping_price_message: str):
        try:
            if shipping_price_message.lower().__contains__("free"):
                return 0
            else:
                return shipping_price_message.replace("$", "").split()[0]
        except Exception:
            return shipping_price_message

    @staticmethod
    def status_analise(in_stock_status):
        if in_stock_status.lower().__contains__("in stock"):
            return 1
        return 0

    @staticmethod
    def time_calculator(shipping_time_message: str):
        try:
            now = datetime.datetime.now()
            if shipping_time_message.split()[-2] == "-":
                shipping_month = datetime.datetime.strptime(
                    shipping_time_message.split()[0], "%b"
                ).month
            else:
                shipping_month = datetime.datetime.strptime(
                    shipping_time_message.split()[-2], "%b"
                ).month
            shipping_day = int(shipping_time_message.split()[-1])
            return (
                datetime.date(now.year, shipping_month, shipping_day)
                - datetime.date(now.year, now.month, now.day)
            ).days
        except Exception:
            return shipping_time_message

    @staticmethod
    def clean_ratings_feedbacks(data: list):
        try:
            for info in data:
                info[0] = info[0].split()[0].replace("(", "")
                info[1] = info[1].split()[0].replace("%", "")
            return data
        except Exception:
            return data


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AmazonSpider)
    process.start()
