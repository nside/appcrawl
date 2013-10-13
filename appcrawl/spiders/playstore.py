from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from appcrawl.items import AppItem, AppStoreItem
from scrapy.http import Request
import datetime
import re

class PlaystoreSpider(CrawlSpider):

    def gen_urls():
      for c in ('ARCADE', 'BRAIN', 'CARDS', 'CASUAL', 'GAME_WALLPAPER', 'RACING', 'SPORTS_GAMES', 'GAME_WIDGETS', 'BOOKS_AND_REFERENCE', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'EDUCATION', 'ENTERTAINMENT', 'FINANCE', 'HEALTH', 'LIBRARIES_AND_DEMO', 'LIFESTYLE', 'APP_WALLPAPER', 'MEDIA_AND_VIDEO', 'MEDICAL', 'MUSIC_AND_AUDIO', 'NEWS_AND_MAGAZINES', 'PERSONALIZATION', 'PHOTOGRAPHY', 'PRODUCTIVITY', 'SHOPPING', 'SOCIAL', 'SPORTS', 'TOOLS', 'TRANSPORTATION', 'TRAVEL_AND_LOCAL', 'WEATHER', 'APP_WIDGETS'):
        yield 'https://play.google.com/store/apps/category/%s/collection/topselling_paid' % c
        yield 'https://play.google.com/store/apps/category/%s/collection/topselling_free' % c

    name = 'playstore'
    allowed_domains = ['play.google.com']
    start_urls = gen_urls()
    reg_start = re.compile('start=([\d]+)')

    rules = (
        #Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r'category/[A-Z_]+\?', deny=r'/accounts/'), follow=True, callback='parse_app'), #categories
#        Rule(SgmlLinkExtractor(allow=r'start=[\d]+&num=[\d]+', deny=r'/accounts/'), follow=True), #categories
        Rule(SgmlLinkExtractor(allow=r'/collection/', deny=r'editors_choice'), follow=True), #categories
        #parse_app
    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        m = PlaystoreSpider.reg_start.search(response.url)
        start = 0
        if m:
          start = int(m.group(1))

        artworks = hxs.select('//div[@class="thumbnail-wrapper goog-inline-block"]/a/img/@src').extract()
        ids = hxs.select('//li[@class="goog-inline-block"]/@data-docid').extract()
        ids += hxs.select('//li[@class="goog-inline-block z-last-child"]/@data-docid').extract() #scary!
        names = hxs.select('//div[@class="details goog-inline-block"]/div/a/text()').extract()
        urls = hxs.select('//div[@class="details goog-inline-block"]/div/a/@href').extract()
        reg_cat = re.compile('/category/([\w_]+)(/|\?|/)*')
        category = reg_cat.search(response.url).group(1).replace('_', ' ').title()
        sellers = hxs.select('//span[@class="attribution"]/div/a').extract()
        seller_links = hxs.select('//span[@class="attribution"]/div/a/@href').extract()

        assert not "We're sorry" in response.body
        assert len(artworks) == len(ids) == len(names) == len(urls) == len(sellers) == len(seller_links), (len(artworks) , len(ids) , len(names) , len(urls)  , len(sellers) , len(seller_links))
        for artwork, id, name, url, seller, seller_link in zip(artworks, ids, names, urls, sellers, seller_links):
          i = AppStoreItem()
          i['store'] = 'play'
          i['id'] = id
          i['artwork'] = artwork
          i['category'] = category
          i['url'] = 'https://play.google.com' + url
          i['name'] = name
          i['last_update'] = datetime.date.today().isoformat()
          i['seller'] = seller
          i['seller_link'] = 'https://play.google.com' + seller_link
          yield i

        if start == 0:
          prefix = '?'
          if '?' in response.url:
            prefix = '&'
          for i in range(24, 480 + 1, 24):
            yield Request(response.url + prefix + 'start=%d&num=24' % i)
