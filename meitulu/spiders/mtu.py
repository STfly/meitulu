# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
i = 1
class MtuSpider(CrawlSpider):
    name = 'mtu'
    allowed_domains = ['www.meitulu.cn']
    # start_urls = ['http://www.meitulu.cn/']
    start_urls = ['http://www.meitulu.cn/item/5514.html']

    rules = (
        # Rule(LinkExtractor(allow=r'http://www.meitulu.cn/t/(.*?)/'), follow=True),  # 要不要都是爬全站
        Rule(LinkExtractor(allow=r'/item/(.*?).html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/item/5514(.*?).html'), callback='parse_item', follow=True),
        # 拦截不全的url补全,自定义下载中间件修改，使用request._set_url(url)
    )

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
