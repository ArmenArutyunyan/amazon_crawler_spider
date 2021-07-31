# Scrapy settings for amazon_crawler_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "amazon_crawler_spider"

SPIDER_MODULES = ["amazon_crawler_spider.spiders"]
NEWSPIDER_MODULE = "amazon_crawler_spider.spiders"

# MongoDB settings
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "amazon"
MONGO_COLLECTION = "amazon_items"

# ScraperAPI key
API_KEY = "0ced624e6d9b220396b7493bb8055f32"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5
RETRY_TIMES = 3

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "amazon_crawler_spider.middlewares.AmazonCrawlerSpiderDownloaderMiddleware": 543,
    "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "amazon_crawler_spider.pipelines.AmazonCrawlerSpiderPipeline": 300,
    "amazon_crawler_spider.pipelines.JsonWriterPipeline": 300
}

ROTATING_PROXY_LIST = [
    "https://armen0788_gmail_com:a472b6e950@84.54.8.191:30030",
    "https://armen0788_gmail_com:a472b6e950@84.54.11.44:30030",
    "https://armen0788_gmail_com:a472b6e950@84.54.8.35:30030",
    "https://armen0788_gmail_com:a472b6e950@84.54.11.14:30030",
    "https://armen0788_gmail_com:a472b6e950@5.182.118.190:30030",
    "https://armen0788_gmail_com:a472b6e950@5.182.119.111:30030",
    "https://armen0788_gmail_com:a472b6e950@5.182.119.202:30030",
    "https://armen0788_gmail_com:a472b6e950@5.182.119.79:30030",
    "https://armen0788_gmail_com:a472b6e950@45.90.199.222:30030",
    "https://armen0788_gmail_com:a472b6e950@45.90.198.27:30030",
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'amazon_crawler_spider.middlewares.AmazonCrawlerSpiderSpiderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'