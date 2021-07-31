# Amazon Product Scraper

Scraper has following features:
* rotates proxy servers from proxy pool *(if needed ScraperAPI calls can be made by taking **Request** line out of comment)*.
* proxy servers are listed in `settings` and are rotated using `scrapy-rotating-proxies` package
* `mongodb` is set up for storing data *(this is done for demonstration purposes as during interview we talked about it)*. 
* `mongodb` host and port can be configured from `settings.py`

Given the id of the item scraper extracts following fields:
* title
* description
* price
* in_stock *(1 if in_stock status is True, 0 if product's out of stock)*
* shipping_price
* shipping_time
* offer_listing 
  * price
  * shipping_time
  * shipping_price
  * total_rating
  * positive_feedback
  * condition


# Getting Started

Script can be run either by using ` scrapy crawl amazon_spider` command or running `amazon_spider.py` itself.
After running the script user will be asked to provide item_id in one of the following form:
* item_id ( e.g B07Y91V9BK )
* multiple item_ids seperated by comma ( e.g. B07Y91V9BK,B08KYNL6LH)
* full path of a text file which has item_ids listed as rows

As a result the aforementioned fields will be extracted and written in a JSON file named `amazon_spider.json` in spiders directory