import psycopg2
import sys
import os
 
def main():
	is_prod = os.environ.get('IS_HEROKU', None)
	
	print("is prod?? ", is_prod),

	if is_prod:
		#Define our connection string
		host = os.environ['DB_HOST']
		dbname = os.environ['DB_NAME']
		user = os.environ['DB_USER']
		password = os.environ['DB_PASSWORD']
		conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host,dbname,user,password)
		# print the connection string we will use to connect
		print("Connecting to database\n	->%s" % (conn_string))
	
		# get a connection, if a connect cannot be made an exception will be raised here
		conn = psycopg2.connect(conn_string)
	
		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor()
		print("Connected!\n")
	else:
		host = 'localhost'
		dbname = 'arsenal_bot'
		user = 'nic'
		#Define our connection string
		conn_string = "host='{}' dbname='{}' user='{}'".format(host,dbname,user)
	
		# print the connection string we will use to connect
		print("Connecting to database\n	->%s" % (conn_string))
	
		# get a connection, if a connect cannot be made an exception will be raised here
		conn = psycopg2.connect(conn_string)
	
		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor()
		print("Connected!\n")
 
if __name__ == "__main__":
	main()