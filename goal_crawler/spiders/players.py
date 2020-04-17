import scrapy
from scrapy.http import Request
from goal_crawler.items import TeamItem, PlayerItem
import unicodedata
class AllteamsSpider(scrapy.Spider):
    name = 'allTeams'
    # allowed_domains = ['https://www.goal.com/en/all-competitions']
    start_urls = ['https://www.goal.com/en/all-competitions/']

    def parse(self, response):
        acs=response.xpath('//p[@class="part-title clearfix"][.="Club"]//following-sibling::ul')
        countries=response.xpath('//p[@class="part-title clearfix"][.="Club"]//following-sibling::div[@class="widget-competitions-list-of-all__group"]/span/text()').extract()
        for i in range(len(countries)):
            leagues=acs[i].xpath('./li/a')
            for league in leagues:
                competition_url=league.xpath('./@href').extract_first()
                competition_name=league.xpath('./span/text()').extract_first()
                country=countries[i]
                yield Request('https://www.goal.com'+competition_url, callback=self.parse_competition)

    def parse_competition(self, response):
        standing=response.xpath('//div[@class="nav-tabs clearfix"]/a[.="Standings"]')
        if len(standing)!=0:
            table_url=standing[0].xpath('./@href').extract_first()
            yield Request('https://www.goal.com'+table_url, callback=self.parse_team)


    def parse_team(self, response):
        teams=response.xpath('//tbody/tr')
        league=response.xpath('//*[@class="text page-header--dropdown dropdown__label"]/text()').extract_first()
        print(len(teams))
        for team in teams:
            url='https://www.goal.com'+team.xpath('.//a[@class="p0c-competition-tables__link"]/@href').extract_first()
            yield Request(url, callback=self.parse_player)

    def parse_player(self, response):
        list_items=response.xpath('//li[@class="p0c-team-squad__member"]')
        club=response.xpath('//*[@class="text"]/text()').extract_first()
        for item in list_items:
            name=item.xpath('.//span[@class="p0c-team-squad__member-name"]/text()').extract_first()
            p_item=PlayerItem()
            p_item['club']=self.strip_accents(club)
            p_item['name']=self.strip_accents(name)
            p_item['last_name']=self.strip_accents(name.split()[-1])
            age=item.xpath('.//span[@class="p0c-team-squad__member-age"]/text()').extract_first()
            if age.split()[-1]=='Age':
                p_item['age']=None
            else:
                p_item['age']=int(age.split()[-1])
            if len(item.xpath('.//a/@href').extract())==0:
                p_item['url']='#'
            else:
                p_item['url']='https://www.goal.com'+item.xpath('.//a/@href').extract_first()
            p_item['img']=item.xpath('.//img/@src').extract_first()
            yield p_item

    def strip_accents(self, text):

        
        text = unicodedata.normalize('NFD', text)\
            .encode('ascii', 'ignore')\
            .decode("utf-8")

        return str(text)


