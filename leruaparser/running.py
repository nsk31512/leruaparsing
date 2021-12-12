from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruaparser import settings
from leruaparser.spiders.lerua import LeruaSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    search_request = input('Введите поисковый запрос: ')
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaSpider, search=search_request)

    process.start()
