import scrapy


class MobileelectroSpider(scrapy.Spider):
    name = "amazon3C"
    start_urls = [
        'https://www.amazon.cn/dp/B010L4HDX6?_encoding=UTF8&ref_=pc_cxrd_760233051_recTab_760239051_t_1&pf_rd_p=96f44de6-4e26-4473-937e-686804be9330&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=760233051&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=T2CQQ0PJE9WCXMES1GMS&pf_rd_r=T2CQQ0PJE9WCXMES1GMS&pf_rd_p=96f44de6-4e26-4473-937e-686804be9330',
    ]

    def parse(self, response):

            yield {
                'title': response.xpath('//span[(@id = "productTitle")]/text()').extract_first().strip(),
                'price': response.xpath('//span[(@id = "priceblock_ourprice")]/text()').extract_first().strip(),
                'origin_price': response.xpath('//td[(@class = "a-span12 a-color-secondary a-size-base")]/text()').extract_first().strip(),
                'comment_num': response.xpath('//span[(@id = "acrCustomerReviewText")]/text()').extract_first().strip(),
                'rating': response.xpath('//span[(@class = "a-icon-alt")]/text()').extract_first().strip()
            }

            comment_page = response.xpath('//a[(@data-hook = "see-all-reviews-link-foot")]/@href').extract_first().strip()

            if comment_page is not None:
                comment_page = response.urljoin(comment_page)
                yield scrapy.Request(comment_page, callback=self.parse_comment)


    def parse_comment(self, response):
        review_list = response.xpath('//div[(@data-hook = "review")]')
        for review in review_list:
            yield {
                'review_author': review.xpath('div/div/span/a[(@data-hook = "review-author")]/text()').extract_first().strip(),
                'review_star': review.xpath('div/div/a/i[(@data-hook = "review-star-rating")]/span/text()').extract_first().strip(),
                'review_body': review.xpath('div/div/span[(@data-hook = "review-body")]/text()').extract_first().strip(),
                'review_date': review.xpath('div/div/span[(@data-hook = "review-date")]/text()').extract_first().strip(),

            }
        # find next page
        next_page = response.xpath('//li[(@class = "a-last")]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_comment)