import scrapy

class CrawlerItem(scrapy.Item):
    TaxCode = scrapy.Field()
    Firm = scrapy.Field()
    Owner = scrapy.Field()
    OwnerInfo = scrapy.Field()
    Phone = scrapy.Field()
    Status = scrapy.Field()
    Address = scrapy.Field()