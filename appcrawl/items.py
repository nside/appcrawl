from scrapy.item import Item, Field

class AppItem(Item):
  id = Field()
  category = Field()
  url = Field()
  name = Field()
  last_update = Field()
  store = Field()

class AppStoreItem(AppItem):
  is_iphone = Field()
  is_ipad = Field()
  is_ipod = Field()
  description = Field()
  artwork = Field()
  subcategory = Field()
  price = Field()
  release_date = Field()
  version = Field()
  size = Field()
  languages = Field()
  seller = Field()
  seller_link = Field()
  copyright = Field()
  rating = Field()
  requirements = Field()
  reviews = Field()
  screenshots = Field()
