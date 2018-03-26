# -*- coding: utf-8 -*-
import scrapy
from yahoo.spiders import FILTER


class FinanceSpider(scrapy.Spider):
	name = 'finance'
	allowed_domains = ['info.finance.yahoo.co.jp']
	url = 'https://info.finance.yahoo.co.jp/history/?code=998407.O&sy=\
		{f_year}&sm={f_mon}&sd={f_day}&ey={t_year}&em={t_mon}&ed={t_day}&tm={resolution}&p=1/'

	custom_settings = {
		'FEED_URI': 'tmp/nikkei_2018.csv'
	}

	def __init__(self):
		self.start_urls = [self.url.format(**FILTER)]

	def parse(self, response):
		table = response.xpath('//*[@class="padT12 marB10 clearFix"]/table').xpath('tr')
		time_id = table.xpath('th[1]/text()').extract_first()
		first_value = table.xpath('th[2]/text()').extract_first()
		max_value = table.xpath('th[3]/text()').extract_first()
		min_value = table.xpath('th[4]/text()').extract_first()
		last_value = table.xpath('th[5]/text()').extract_first()
		for tr in table:			
			if not tr.xpath('td[1]/text()').extract_first():
				continue
			yield {
				time_id: tr.xpath('td[1]/text()').extract_first(),
				first_value: tr.xpath('td[2]/text()').extract_first(),
				max_value: tr.xpath('td[3]/text()').extract_first(),
				min_value: tr.xpath('td[4]/text()').extract_first(),
				last_value: tr.xpath('td[5]/text()').extract_first()
			}
		# tmp = int(response.xpath('//ul/span/text()').extract_first())		
		next_page =  response.xpath('//*[@id="main"]/ul/a/@href').extract()[-1]
		next_text =  response.xpath('//*[@id="main"]/ul/a/text()').extract()
		if next_page is not None:
			if u'次へ' in next_text:			
				yield response.follow(next_page, callback=self.parse)

