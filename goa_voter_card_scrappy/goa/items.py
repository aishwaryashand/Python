# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoaItem(scrapy.Item):
    # define the fields for your item here like:
    ac_value = scrapy.Field()
    ac_name = scrapy.Field()
    table_name = scrapy.Field()
    ps_name = scrapy.Field()
    ps_pdf_link = scrapy.Field()
    pdf_path = scrapy.Field()
    pdf_downloaded = scrapy.Field()
