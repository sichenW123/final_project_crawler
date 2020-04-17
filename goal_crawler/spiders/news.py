import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest
from goal_crawler.items import NewsItem
import re
import datetime
from dateutil.parser import *
import unicodedata


class SinglepageSpider(scrapy.Spider):
    name = 'singlepage'
    # allowed_domains = ['goal.com/en/']
    start_urls = ['https://goal.com/en/news/151']

    def parse(self, response):
        url=response.url.split("/")
        page=int(url[-1])
        print(page)
        if page<300:
            articles=response.xpath('//article')
            for article in articles:
                url=article.xpath('.//a/@href').extract_first()
                link=response.urljoin(url)
                frag=link.split('/')
                if frag[4]=='news' and frag[5]!='live':
                    yield SplashRequest(url=link, callback=self.parse_news, endpoint='render.html')
            next_page=response.xpath('//*[@class="btn btn--older needsclick"]/@href').extract_first()
            abs_next_page=response.urljoin(next_page)
            yield Request(abs_next_page, callback=self.parse)

    def parse_news(self, response):
        img=response.xpath('//div[@class="picture article-image"]/noscript/img/@src').extract_first()
        if img is None:
            img=response.xpath('//div[@class="picture article-image"]/noscript/text()').extract_first()
            img=img.split()[1][5:-1]
        tags=response.xpath('//*[@class="tags-list__link"]/text()').extract()
        ts=[]
        for tag in tags:
            ts.append(self.strip_accents(tag.strip()))
        title=self.strip_accents(response.xpath('//*[@class="article-headline"]/text()').extract_first())
        date=response.xpath('//*[@class="actions-bar__time publish-date"]/span/text()').extract()
        # date=date.strip()
        date=datetime.datetime.strptime(date[1].strip(), '%d/%m/%Y')
        #date=parse(date[1].strip())
        contents=response.xpath('//p[not(@class)]//text()').extract()
        content=''
        for c in contents:
            content=c+' '+content
        content=self.strip_accents(content)
        new_content=re.sub(r'/<[^>]+>/g','', content)
        item=NewsItem()
        item['url']=response.url
        item['img']=img
        item['title']=title
        item['tags']=ts
        item['date']=date
        item['content']=new_content
        yield item


    def strip_accents(self, text):

        
        text = unicodedata.normalize('NFD', text)\
            .encode('ascii', 'ignore')\
            .decode("utf-8")

        return str(text)