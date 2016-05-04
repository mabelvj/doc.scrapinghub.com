import scrapy


class SpidyquotesSpider(scrapy.Spider):
    name = "spidyquotes"
    allowed_domains = ["spidyquotes.herokuapp.com"]
    start_urls = [
        'http://spidyquotes.herokuapp.com/',
    ]
    download_delay = 2.5

    def parse(self, response):
        for quote in response.css('.quote'):
            yield {
                'text': quote.css('span::text').extract_first(),
                'author': quote.css('small::text').extract_first(),
                'tags': quote.css('.tags a::text').extract(),
            }
        link_next = response.css('li.next a::attr("href")').extract_first()
        if link_next:
            yield scrapy.Request(response.urljoin(link_next))
