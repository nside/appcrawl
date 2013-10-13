# Scrapy settings for appcrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'appcrawl'
BOT_VERSION = '1.0'
LOG_ENABLED = False
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

SPIDER_MODULES = ['appcrawl.spiders']
NEWSPIDER_MODULE = 'appcrawl.spiders'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1'
USER_AGENT_LIST = (
  "AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
)

HTTPCACHE_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
  'appcrawl.random_user_agent.RandomUserAgentMiddleware': 400,
  'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
  'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware' : None,
}

#FEED_URI = 'file:///Users/dlaprise/apprs/appcrawl/apps.json'
#FEED_FORMAT =  'json'

RETRY_HTTP_CODES =  [500, 503, 504, 400, 408, 403]

