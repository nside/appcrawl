from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from appcrawl.items import AppItem, AppStoreItem
import datetime

class AppstoreSpider(CrawlSpider):
    name = 'appstore'
    allowed_domains = ['itunes.apple.com']
    start_urls = ['http://itunes.apple.com/us/genre/ios-books/id6018?mt=8',
                  'http://itunes.apple.com/us/genre/ios-business/id6000?mt=8',
                  'http://itunes.apple.com/us/genre/ios-catalogs/id6022?mt=8',
                  'http://itunes.apple.com/us/genre/ios-education/id6017?mt=8',
                  'http://itunes.apple.com/us/genre/ios-entertainment/id6016?mt=8',
                  'http://itunes.apple.com/us/genre/ios-finance/id6015?mt=8',
                  'http://itunes.apple.com/us/genre/ios-food-drink/id6023?mt=8',
                  'http://itunes.apple.com/us/genre/ios-games/id6014?mt=8',
                  'http://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8',
                  'http://itunes.apple.com/us/genre/ios-lifestyle/id6012?mt=8',
                  'http://itunes.apple.com/us/genre/ios-medical/id6020?mt=8',
                  'http://itunes.apple.com/us/genre/ios-music/id6011?mt=8',
                  'http://itunes.apple.com/us/genre/ios-navigation/id6010?mt=8',
                  'http://itunes.apple.com/us/genre/ios-news/id6009?mt=8',
                  'http://itunes.apple.com/us/genre/ios-newsstand/id6021?mt=8',
                  'http://itunes.apple.com/us/genre/ios-photo-video/id6008?mt=8',
                  'http://itunes.apple.com/us/genre/ios-productivity/id6007?mt=8',
                  'http://itunes.apple.com/us/genre/ios-reference/id6006?mt=8',
                  'http://itunes.apple.com/us/genre/ios-social-networking/id6005?mt=8',
                  'http://itunes.apple.com/us/genre/ios-sports/id6004?mt=8',
                  'http://itunes.apple.com/us/genre/ios-travel/id6003?mt=8',
                  'http://itunes.apple.com/us/genre/ios-utilities/id6002?mt=8',
                  'http://itunes.apple.com/us/genre/ios-weather/id6001?mt=8',
    ]

    rules = (
       Rule(SgmlLinkExtractor(allow='letter=[\w\*]+'), follow=True, callback="parse_applist"),
       Rule(SgmlLinkExtractor(allow='letter=[\w\*]+\&page=[\d]+'), follow=True, callback="parse_applist"),
    )

    def parse(self, response):
      r = list(CrawlSpider.parse(self, response))
      return r + list(self.parse_applist(response))


    def parse_applist(self, response): #parse_applist
      hxs = HtmlXPathSelector(response)
      category = hxs.select('//title/text()').extract()[0].split('-')[0].strip()
      idx = 0
      for url, name in zip(hxs.select('//div[contains(@class,"column")]/ul/li/a/@href').extract(), hxs.select('//div[contains(@class,"column")]/ul/li/a/text()').extract()):
        if not '/app/' in url:
          continue
        i = AppItem()
        i['name'] = name
        i['url'] = url
        i['id'] = url.split('/')[-1].split('?')[0]
        i['category'] = category
        i['last_update'] = datetime.date.today().isoformat()
        i['store'] = 'appstore'
        idx += 1
        yield i

    def parse_app(self, response): #parse_app
      hxs = HtmlXPathSelector(response)
      i = AppStoreItem()
      i['name'] = hxs.select('//div/div/h1/text()').extract()[0]
      i['url'] = response.url
      i['id'] = response.url.split('/')[-1].split('?')[0]
      attrs = hxs.select('//div[@id="content"]')
      i['description'] = "\n".join(attrs.select('//div[@class="product-review"]/p/text()').extract())
      i['artwork'] = attrs.select('//div[@class="lockup product application"]/a/div/img/@src').extract()
      i['price'] =  attrs.select('//div[@class="price"]/text()').extract()[0]
      i['release_date'] = attrs.select('//li[@class="release-date"]/text()').extract()[0]
      release_date, version, size, languages, seller, copyright = tuple(attrs.select('//li/text()').extract())[0:6] #hugely unsafe but that's how we roll
      i['release_date'] = release_date
      i['version'] = version
      i['size'] = size
      i['languages'] = languages
      i['seller'] = seller
      seller_link = hxs.select('//div[@class="app-links"]/a/@href').extract()
      if len(seller_link) > 1:
        i['seller_link'] = seller_link[0]
      else:
        i['seller_link'] = ''
      i['copyright'] = copyright
      i['rating'] = attrs.select('//a[@href="http://itunes.apple.com/WebObjects/MZStore.woa/wa/appRatings"]/text()').extract()[0]
      try:
        requirements = attrs.select('//div[@class="lockup product application"]/p/text()').extract()[0]
      except:
        requirements = ''
      i['requirements'] = requirements
      i['reviews'] = ''#todo
      i['screenshots'] = "|".join(hxs.select('//div[@class="swoosh lockup-container application large screenshots"]//img/@src').extract())
      i['is_iphone'] = 'iPhone' in requirements
      i['is_ipad'] = 'iPad' in requirements
      i['is_ipod'] = 'iPod' in requirements
      i['last_update'] = datetime.date.today().isoformat()
      i['store'] = 'appstore'
      yield i

