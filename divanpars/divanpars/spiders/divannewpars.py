import scrapy


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        divans = response.css('div.LlPhw')
        for divan in divans:
            yield {
                'name': divan.css('div.lsooF span::text').get(),
                'price': divan.css('div.q5Uds span::text').get(),
                'url': divan.css('a').attrib['href']
            }

