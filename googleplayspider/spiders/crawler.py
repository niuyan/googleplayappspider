from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import HtmlXPathSelector
from googleplayspider.items import GoogleplayspiderItem
import urllib
import scrapy
import logging

"""
the spider class, which will read and parse the url from Google Play
    and extract the information for @see items.py;
    data crawled will be stored into MongoDB database
"""



class GoogleplayspiderCN(CrawlSpider):
    # define the name of the spider
    name = "GooglePlaySpiderCN"

    # set the allowed domain to crawl
    # see document https://doc.scrapy.org/en/latest/topics/spiders.html
    allowed_domains = ['play.google.com']

    # start_urls to process
    start_urls =[
        "https://play.google.com/store/apps/category/COMMUNICATION",
        "https://play.google.com/store/apps/category/SOCAIL",
        "https://play.google.com/store/apps/category/DATING",
        "https://play.google.com/store/apps/category/TOOLS",
        "https://play.google.com/store/apps/category/VIDEO_PLAYERS",
        "https://play.google.com/store/apps/category/NEWS_AND_MAGAZINES"
    ]

    # define the rule for Crawler
    '''
     please notice that the scrapy will check the first rule and the second, thrid
    '''
    rules = (
        Rule(LinkExtractor(allow=(r'/store/apps/details'), deny=(r'reviewId')), follow=True, callback='gp_parse_link', process_links='gp_process_link'),
        Rule(LinkExtractor(allow=(r'/store/apps/collection')), follow=True),
    )

    def gp_process_link(self, links):
        for link in links:
            if link.url.find('?') == -1:
                link.url = link.url + "?hl=zh-CN"
            else:
                link.url = link.url + "&hl=zh-CN"
        return links

    def gp_parse_link(self, response):

        item = GoogleplayspiderItem()

        item["Name"] = response.xpath('//*[@itemprop="name"]/span/text()').extract_first()
        item["Icon"] = response.xpath('//h1[@itemprop="name"]/../../../../preceding::*[@itemprop="image"]/@src').extract_first()
        item["Link"] = str(response.url)
        item["Genre"] = response.xpath('//*[@itemprop="genre"]/text()').extract_first()
        item["Description"] = str(response.xpath('//meta[@itemprop="description"]/@content').extract_first())
        item["Last_updated"] = str(response.xpath('//div[text()="更新日期"]/following-sibling::*[1]//text()').extract_first())
        item["Installs"] = str(response.xpath('//div[text()="安装次数"]/following-sibling::*[1]//text()').extract_first())
        item["Version"] = str(response.xpath('//div[text()="当前版本"]/following-sibling::*[1]//text()').extract_first())
        item["Content_rating"] = str(response.xpath('//div[text()="内容分级"]/following-sibling::*[1]//text()').extract_first())
        item["Developer"] = str(response.xpath('//div[text()="开发者"]/following-sibling::*//text()').extract())
        item["Review_number"] = response.xpath('//h2[text()="评价"]/following-sibling::*/../..//text()').extract()[4]
        item["Review_rating"] = response.xpath('//h2[text()="评价"]/following-sibling::*/../..//text()').extract()[2]
        item["Offeredby"] = str(response.xpath('//div[text()="提供者："]/following-sibling::*[1]//text()').extract_first())

        #yield item
