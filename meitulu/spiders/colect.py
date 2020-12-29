# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time
i = 1

class MtuSpider(CrawlSpider):
    name = 'mtu2'
    allowed_domains = ['meitulu.cn']  # 注意domain 有些链接不是www开头，无法下载
    # start_urls = ['http://www.meitulu.cn/']
    # start_urls = ['http://www.meitulu.cn/item/5514.html']
    start_urls = []
    # start_urls = [].append(input('请输入图片集的url'))

    rules = (
        Rule(LinkExtractor(allow=r'/item/.*?.html', restrict_xpaths='/html/body/div[2]/div[3]/ul/li/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/item/.*?_.*?.html', restrict_xpaths='//*[@id="pages"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/t/.*?_.*?.html', restrict_xpaths='//*[@id="pages"]/a'), callback='parse_item', follow=True),
        # 拦截不全的url补全,自定义下载中间件修改，使用request._set_url(url)
    )

    def start_requests(self):
        # for url in self.start_urls:
        url = input('请输入起始url')
        # 控制台可以用，pycharm会报错
        # url = 'http://www.meitulu.cn/t/pingye/'
        yield scrapy.Request(url, dont_filter=True)
    def parse_item(self, response):
        global i
        i = i + 1
        print(str(i) + "+++++++" + response.url)
        try:
            pic_url = response.xpath('/html/body/div[@class="content"]/center/a/img/@src').extract_first()
            pic_title = response.xpath('/html/body/div[@class="content"]/center/a/img/@alt').extract_first()
            model_name = response.xpath('/html/body/div[2]/div[2]/p[5]/a/text()').extract_first()
            organ = response.xpath('/html/body/div[2]/div[2]/p[1]/a/text()').extract_first()
            if pic_url != None:
                # print(pic_url)
                item = {'pic_url': pic_url, 'pic_title': pic_title, 'model_name': model_name, 'organ': organ}
                yield item
        except:
            print('无图' + response.url)

