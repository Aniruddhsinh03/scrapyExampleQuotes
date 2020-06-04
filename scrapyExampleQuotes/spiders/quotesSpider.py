# -*- coding: utf-8 -*-
import scrapy


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
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            comment = quote.xpath('.//*[@class="text"]/text()').extract_first()
            tags = quote.xpath('.//*[@class="keywords"]/@content').extract()
            author = quote.xpath('.//*[@class="author"]/text()').extract_first()
            author_link = quote.xpath('.//a/@href').extract_first()

            yield {'Comment': comment, 'Tags': tags, 'Author': author}
            yield scrapy.Request(response.urljoin(author_link), callback=parse_author_contents,
                                 meta={'Comment': comment, 'Tags': tags, 'Author': author})

        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)
