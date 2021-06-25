import scrapy
from ..items import GoaItem
import os

BASE_DIR = os.environ.get('', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIRS = {
	'doc_path': os.path.join(BASE_DIR, 'documents')
}
for value in DIRS.values():
	if not os.path.exists(value):
		os.makedirs(value)

class QuotesSpider(scrapy.Spider):
	name = 'quotes'

	def start_requests(self):
		# global urls
		urls = ['https://ceogoa.nic.in/appln/uil/ElectoralRoll.aspx']
		# global headers
		# headers = {
		# 	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
		# 	'Accept': '*/*',
		# 	'Accept-Language': 'en-US,en;q=0.5',
		# 	'X-Requested-With': 'XMLHttpRequest',
		# 	'X-MicrosoftAjax': 'Delta=true',
		# 	'Cache-Control': 'no-cache',
		# 	'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
		# 	'Origin': 'https://ceogoa.nic.in',
		# 	'Connection': 'keep-alive',
		# 	'Referer': urls[0],
		# }

		yield scrapy.Request(url=urls[0], method='GET', callback=self.parse1)
		# if len(all_ps_names) == len(all_ps_pdf_links):
		# 	# for pdf_link in all_ps_pdf_links:
		# 		yield scrapy.Request(url=all_ps_pdf_links[0], method='GET', callback=self.download, cookies=cookies)

	def parse1(self, response):
		cookies = {"ASP.NET_SessionId":response.headers.getlist('Set-Cookie')[0].decode("utf-8").split(';')[0].split('=')[0]}
		# global all_ps_names
		# global all_ps_pdf_links
		# global ps_pdf_link
		items = GoaItem()
		all_ac_names = [i.split("-")[1] for i in response.css('option::text').getall()[1:]]
		for ac_name in all_ac_names[0:1]:
			items["table_name"] = 'voter_id_goa_assembly_constituencies'
			n = all_ac_names.index(ac_name) + 1
			items["ac_value"] = 'AC'+str(n)
			items["ac_name"] = all_ac_names[n-1]
			# yield items
			# data = {
			# 	'ctl00$ToolkitScriptManager': 'ctl00$ToolkitScriptManager|ctl00$Main$btnSearch',
			# 	'_TSM_HiddenField_': response.css('[id="_TSM_HiddenField_"]::attr(value)').get(),
			# 	'__EVENTTARGET': '',
			# 	'__EVENTARGUMENT': '',
			# 	'__VIEWSTATE': response.css('[id="__VIEWSTATE"]::attr(value)').get(),
			# 	'ctl00$Main$drpAC': 'AC'+str(n),
			# 	'ctl00$Main$vcAC_ClientState': '',
			# 	'ctl00$Main$hdnCaptch': '',
			# 	'ctl00$Main$txtCodeNumberTextBox': '',
			# 	'ctl00$Main$vceLetters_ClientState': '',
			# 	'__ASYNCPOST': 'true',
			# 	'ctl00$Main$btnSearch': 'Search'
			# }
			# yield scrapy.Request(url=urls[0], method='POST', callback=self.parse2, headers=headers, cookies=cookies, meta=data, dont_filter=True)

		# with open('page1.html', 'wb') as f:
		# 		f.write(response.body)
		# self.log(f'Saved file {filename}')
			all_ps_names = [x.strip() for x in response.css('[id="AC{ac_value}"]'.format(ac_value=n)).css('div[class="col-md-9"]::text').getall() if not x.strip() == '']
			all_ps_pdf_links = [x.replace('../..','https://ceogoa.nic.in') for x in response.css('[id="AC{ac_value}"]'.format(ac_value=n)).css('a::attr(href)').getall()]
			all_ps_pdf_links.pop(1)
			for ps_pdf_link in all_ps_pdf_links[0:1]:
				yield scrapy.Request(url=ps_pdf_link, method='GET', callback=self.download, cookies=cookies,meta={'n':n, 'ps_name':all_ps_names[all_ps_pdf_links.index(ps_pdf_link)]})


	def download(self,response):
		items = GoaItem()
		filename = response.url.split('/')[-1]
		final_path = DIRS['doc_path']+'/'+filename
		with open(final_path, 'wb') as f:
			f.write(response.body)
		items['table_name'] = 'voter_id_goa_polling_stations'
		items['ps_name'] = response.meta['ps_name']
		items['pdf_path'] = final_path
		items['ps_pdf_link'] = response.url
		items['pdf_downloaded'] = 1
		yield items
