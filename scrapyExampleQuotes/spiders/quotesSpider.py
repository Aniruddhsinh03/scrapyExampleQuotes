# -*- coding: utf-8 -*-
import scrapy


# store all information at last in yield .
def parse_author_contents(response):
    comment = response.meta['Comment']
    tags = response.meta['Tags']
    author = response.meta['Author']
    author_born_date = response.xpath('//*[@class="author-born-date"]/text()').extract_first()
    author_born_location = response.xpath('//*[@class="author-born-location"]/text()').extract_first()
    author_description = response.xpath('//*[@class="author-description"]/text()').extract_first()
    yield {'Comment': comment, 'Tags': tags, 'Author': author, 'Author Born Date': author_born_date,
           'Author Born Location': author_born_location, 'Author Description': author_description}


class QuotesSpider(scrapy.Spider):
    name = 'quotesSpider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # retrieving all quotes sections in quotes variable
        quotes = response.xpath('//*[@class="quote"]')
        # using for loop retrieving each of quote
        for quote in quotes:
            comment = quote.xpath('.//*[@class="text"]/text()').extract_first()
            tags = quote.xpath('.//*[@class="keywords"]/@content').extract()
            author = quote.xpath('.//*[@class="author"]/text()').extract_first()
            author_link = quote.xpath('.//a/@href').extract_first()

            # each of quote have author information which is hyperlink,so visit that author page.
            # visit author page and call method parse_author_contents for scraping author information.
            yield scrapy.Request(response.urljoin(author_link), callback=parse_author_contents,
                                 meta={'Comment': comment, 'Tags': tags, 'Author': author})

        # retrieving next page url and attach with mail url and visit all pages.
        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)
