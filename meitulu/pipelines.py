# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class MyPipeline(object):
    def process_item(self, item, response):
        content = {'pic_url': item['pic_url'], 'pic_title': item['pic_title'],
                   'model_name': item['model_name'], 'organ': item['organ']}
        data = json.dumps(content, ensure_ascii=False)
        # print(data)
        with open('../mt.json', 'a+')as f:
            f.write(data + '\n')
        return item  # 给后面处理


class MyimagesPipeline(ImagesPipeline):

    # 调用这个函数这要是为了将title传给file_path使用，
    def get_media_requests(self, item, info):
        # 在请求img_url前，在请求中带上title参数,Request要导包
        # print(item)
        yield Request(url=item['pic_url'], meta={'pic_title': item['pic_title'], 'model_name': item['model_name']})

    def file_path(self, request, response=None, info=None):
        image_file = request.meta['model_name'] + '/' + request.meta['pic_title']
        image_name = request.url.split('/')[-1].split('.')[0]
        # 'http://image.meitulu.cn/d/file/bigpic/2016/06/17/01/201606170111523071.jpg'
        # print(image_name, image_file)
        return './%s/%s.jpg' % (image_file, image_name)
