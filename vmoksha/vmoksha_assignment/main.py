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
	try:
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
	except Exception as e:
		print(e)


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
