import mysql.connector


def db_connection():
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="Auth@123",
		database="vmoksha"
	)
	cursor = db.cursor(buffered=True)
	return db,cursor
