import scrapy

from ..items import BooksmongoItem

class BookSpiderSpider(scrapy.Spider):
    name = "books"
    # Define crawling logic
    def start_requests(self):
        url = 'https://prestigebookshop.com/product-category/autobiography/'

        for page in range(1, 24):
            next_page = url + f'page/{str(page)}/'
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse(self, response, **kwargs):
        items = BooksmongoItem()
        # extract data
        for card in response.css('li.type-product'):
            title = card.css('h2.woocommerce-loop-product__title::text').get().encode('ascii', 'ignore').decode('utf-8').strip()
            price = card.css('span.woocommerce-Price-amount::text').get().encode('ascii', 'ignore').decode('utf-8').strip()
            image_url = card.css('.product_image').css('img::attr(data-src)').get()

            items['book_title'] = title
            items['book_price'] = price
            items['image_url'] = image_url

            yield items
