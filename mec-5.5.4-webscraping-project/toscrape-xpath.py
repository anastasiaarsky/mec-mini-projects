import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('string(span[@class="text"])').get(),
                'author': quote.xpath('string(small[@class="author"])').get(),
                'tags': quote.xpath('string(div[@class="tags"]/a[@class="tag"])').get(),
            }

        next_page = response.xpath('//li[@class = "next"]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
