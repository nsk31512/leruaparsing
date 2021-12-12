import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from itemloaders.processors import MapCompose


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://novosibirsk.leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="product-name"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_product)


    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath('name', '//h1//text()')
        loader.add_xpath('_id', '//div[@data-testid="product-title_mf-pdp"]//span/text()[2]')
        loader.add_xpath('price', '//showcase-price-view[@slot="primary-price"]/span[1]/text()',
                         MapCompose(lambda x: x.replace('\xa0', '')))
        loader.add_css('photos', 'picture source[media*="1024"][srcset*="https"]', re=r'http.+jpg')
        loader.add_value('url', response.url)
        yield loader.load_item()
