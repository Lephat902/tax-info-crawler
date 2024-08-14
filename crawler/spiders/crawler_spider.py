from scrapy_splash import SplashRequest
from scrapy import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem

class CrawlerSpider(Spider):
    BASE_DOMAIN = "masothue.com"
    BASE_URL_PATH = f"https://{BASE_DOMAIN}"
    name = "crawler"
    allowed_domains = [BASE_DOMAIN, "0.0.0.0"]
    num_of_pages_to_fetch = 1  # change it to your desired number of pages (25 items per page)

    def __init__(self):
        # used lambda func to not pollute the namespace
        get_start_urls = lambda num_of_pages_to_fetch: [f"{self.BASE_URL_PATH}/tra-cuu-ma-so-thue-theo-tinh/ho-chi-minh-23?page={i}" for i in range(1, num_of_pages_to_fetch + 1)]
        self.start_urls = get_start_urls(self.num_of_pages_to_fetch)

    def start_requests(self):
        # Use SplashRequest for the initial request
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, args={'wait': 1})

    def parse(self, response):
        tax_info_records = Selector(text=response.text).css('main > section > div > div.tax-listing > div:nth-child(n)')

        for rec in tax_info_records:
            urlToFirm = self.BASE_URL_PATH + '/' + rec.css('h3 > a::attr(href)').get()
            
            # Use SplashRequest to handle JavaScript and wait for the page to fully render
            yield SplashRequest(
                urlToFirm,
                callback=self.parse_firm_detail,
                args={'wait': 3}
            )

    def parse_firm_detail(self, response):
        tax_info_tbl = Selector(response).css('main > section:nth-child(n) > div > table.table-taxinfo')

        item = CrawlerItem()
        item['Firm'] = tax_info_tbl.css('thead > tr > th > span::text').get()

        detail = tax_info_tbl.css('tbody')[0]
        
        item['TaxCode'] = detail.css('tr:nth-child(n) > td[itemprop="taxID"] > span::text').get()
        item['Address'] = detail.css('tr:nth-child(n) > td[itemprop="address"] > span::text').get()
        item['Owner'] = detail.css('tr[itemprop="alumni"] > td:nth-child(2) > span > a::text').get()
        owner_info = detail.css('tr[itemprop="alumni"] > td:nth-child(2)::text')
        item['OwnerInfo'] = "" if len(owner_info) < 2 else owner_info[1].get()
        item['Phone'] = detail.css('tr:nth-child(n) > td[itemprop="telephone"] > span::text').get()
        item['Status'] = detail.css('tr:nth-child(n) > td:nth-child(2) > a[title="tra cứu mã số thuế công ty Đang hoạt động (đã được cấp GCN ĐKT)"]::text').get()

        yield item

