# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class NewsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection=table='news'
    url=Field()
    title=Field()
    img=Field()
    tags=Field()
    date=Field()
    content=Field()


class TeamItem(Item):
    collection=table='teams'
    url=Field()
    name=Field()
    league=Field()
    img=Field()
    abbr=Field()


class PlayerItem(Item):
    collection=table='players'
    name=Field()
    age=Field()
    img=Field()
    url=Field()
    club=Field()
    last_name=Field()
    
