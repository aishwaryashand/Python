# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class GoaPipeline(object):
	def __init__(self):
		self.create_connection()
		# self.create_table()

	def create_connection(self):
		self.conn = mysql.connector.connect(
			host="127.0.0.1",
			user="root",
			passwd="Auth@123",
			database="voter_id"
		)
		self.cursor = self.conn.cursor(buffered=True)
		#self.cursor.execute("""ALTER TABLE `voter_id`.`voter_id_goa_assembly_constituencies` CHANGE COLUMN `pdf_dowloaded` `pdf_downloaded` TINYINT NULL DEFAULT '0' ; """)
		#self.cursor.execute("""ALTER TABLE `voter_id`.`voter_id_goa_polling_stations` CHANGE COLUMN `pdf_dowloaded` `pdf_downloaded` TINYINT NULL DEFAULT '0' ; """)
		#self.conn.commit()



	# def create_table(self):
	# 	self.cursor.execute("""CREATE TABLE IF NOT EXISTS voter_id_goa_assembly_constituencies(
	# 		id BIGINT(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	# 		ac_value VARCHAR(100) DEFAULT NULL,
	# 		ac_name VARCHAR(100) DEFAULT NULL,
	# 		pdf_dowloaded INT(10) DEFAULT 0,
	# 		created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	# 		);""")
	# 	self.cursor.execute("""CREATE TABLE IF NOT EXISTS voter_id_goa_polling_stations(
	# 		id BIGINT(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	# 		ac_table_id BIGINT(10) UNSIGNED DEFAULT NULL,
	# 		ps_name VARCHAR(100) DEFAULT NULL,
	# 		pdf_path VARCHAR(500) DEFAULT NULL,
	# 		ps_pdf_link VARCHAR(500) DEFAULT NULL,
	# 		pdf_dowloaded INT(10) DEFAULT 0,
	# 		created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	# 		updated_on TIMESTAMP DEFAULT NULL,
	# 		FOREIGN KEY (ac_table_id) REFERENCES voter_id_goa_assembly_constituencies (id)
	# 		);""")



	def process_item(self, item, spider):
		if item['table_name'] == 'voter_id_goa_assembly_constituencies':
			self.insert_ac(item)
		elif item['table_name'] == 'voter_id_goa_polling_stations':
			self.insert_ps(item)
		return item


	def insert_ac(self,item):
		self.cursor.execute("""SELECT * from voter_id_goa_assembly_constituencies WHERE ac_value = %s and ac_name = %s""",(item['ac_value'],item['ac_name'],))
		if self.cursor.fetchone() == None:
			self.cursor.execute("""INSERT INTO  voter_id_goa_assembly_constituencies (ac_value, ac_name) VALUES (%s,%s)""",(item['ac_value'],item['ac_name'],))
			self.conn.commit()

	def insert_ps(self,item):
		fk_id = item['ps_pdf_link'].split('/')[-2]
		self.cursor.execute("""SELECT * from voter_id_goa_polling_stations WHERE ps_pdf_link = %s""",(item['ps_pdf_link'],))
		db_records = self.cursor.fetchone()
		if db_records == None:
			self.cursor.execute("""INSERT INTO  voter_id_goa_polling_stations (ac_table_id, ps_name,ps_pdf_link,pdf_path,pdf_downloaded) VALUES (%s,%s,%s,%s,%s)""",(fk_id,item['ps_name'],item['ps_pdf_link'],item['pdf_path'],item['pdf_downloaded']))
			self.conn.commit()
		else:
			if not db_records[3] == item['pdf_path']:
				self.cursor.execute("""UPDATE voter_id_goa_polling_stations SET pdf_path = %s where ps_pdf_link = %s""",(item['pdf_path'],item['ps_pdf_link']))
				self.conn.commit()
