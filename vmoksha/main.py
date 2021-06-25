import requests
from bs4 import BeautifulSoup
from database import db_connection

def strings_to_num(argument):   
	switcher = { 
			'dc': '+',
			'fe': '(',
			'hg': ')',
			'ba': '-',
			'acb': '0', 
			'yz': '1', 
			'wx': '2',
			'vu': '3',
			'ts': '4',
			'rq': '5',
			'po': '6',
			'nm': '7',
			'lk': '8',
			'ji': '9'
	} 
	return switcher.get(argument)

def main():

	for page in range(1,51):
		print("On page "+str(page))
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'Cache-Control': 'max-age=0',
			'TE': 'Trailers',
		}
		response = requests.get('https://www.justdial.com/Bangalore/Ayurvedic-Doctors/nct-10029616/page-{}'.format(page), headers=headers)
		cookies = response.cookies.get_dict()
		soup = BeautifulSoup(response.content,'html.parser')
		store_details = soup.findAll('div',{'class':'store-details'})
		for store_detail in store_details:
			store_name = store_detail.find('a')['title']
			store_address = store_detail.find('span',{'class':'cont_fl_addr'}).text
			contact_details = store_detail.findAll('span',{'class':'mobilesv'})
			myList = []
			for contact in contact_details:
				myString = contact['class'][1].split("-")[1]
				myList.append(strings_to_num(myString))
			contact = "".join(myList)
			print(store_name)
			print(store_address)
			print(contact)
			entry_db(store_name,store_address,contact)

		# all_links = soup.findAll('a',{'class':'nlogo lazy srtbyPic'})
		# for link in all_links:
		# 	link_scraping(link['href'],cookies)


def link_scraping(link,cookies):
	print(link)
	detailmodule = link.split("/")[-1].split("?")[0].split("_")[0].replace("-",".")
	cookies["_fbp"] = "fb.1.1620476579698.239085513"
	cookies["_ga"] = "GA1.2.736368300.1620476578"
	cookies["_gat"] = "1"
	cookies["_gat_UA-31027791-3"] = "1"
	cookies["_gid"] = "GA1.2.1919320898.1620476578"
	cookies["bd_inputs"] = "7|6|Ayurvedic Doctors"
	cookies["bdapop"] = "080PXX80.XX80.110623165821.F8V7"
	cookies["BDprofile"] = "1"
	cookies["bm_sv"] = "62DFDCAB97796B69E4FACF7F77CE12DC~PQALCwUg2UlOq1bJMrxPLtC6ic7LgNYypUQ5I5rQwpVyy24e71DiOnk385PWk66JWoiX+qVHhEvntUYWly57zUwv4PIo3yGGX9fP4qu8+r8aghxI9DNdUiTr7ruYLG4hojPm/t4NgaRiPCdd0iCjuontVfN8ZJFtStyAONez1H0="
	cookies["dealBackCity"] = "Bangalore"
	cookies["detailmodule"] = detailmodule
	cookies['docidarray'] = '%7B%22080PXX80.XX80.110623165821.F8V7%22%3A%222021-05-09%22%2C%22080PXX80.XX80.160211114414.Y2Z6%22%3A%222021-05-09%22%2C%22080PXX80.XX80.210304115757.X1N1%22%3A%222021-05-09%22%2C%22{}%22%3A%222021-05-09%22%7D'.format(detailmodule)
	cookies["prevcatid"] = "10029616"
	cookies["sarea"] = ""
	cookies["scity"] = "Bangalore"
	cookies["tab"] = "toprs"
	cookies["view"] = "lst_v"

	response = requests.get(link.split("&",-1)[0], headers=headers, cookies=cookies)
	soup = BeautifulSoup(response.content,'html.parser')
	# find_mo = soup.find('span',{'class':'telnowpr'})
	# print(find_mo.text)
	find_b_name = soup.find('span',{'class':'fn'})
	if find_b_name != None:business_name = find_b_name.text.strip()
	else: business_name = "NA"
	find_address = soup.find('span',{'id':'fulladdress'})
	if find_address != None: address = find_address.text.split("(Map)")[0].strip()
	else: address = "NA"
	print(business_name)
	print(address)
	if business_name != "NA":
		entry_db(business_name,address)
	else:
		exit()

def entry_db(business_name,address,contact):
	db,cursor = db_connection()
	cursor.execute("SELECT * from bangalore_ayurvedic_doctors where business_name = %s and address = %s and mobile_number = %s",(business_name,address,contact))
	record = cursor.fetchall()
	if record == []:
		cursor.execute("INSERT INTO bangalore_ayurvedic_doctors (business_name,address,mobile_number) VALUES (%s,%s,%s)",(business_name,address,contact))
		db.commit()
	db.close()


if __name__ == '__main__':
	main()
