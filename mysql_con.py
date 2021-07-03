import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", passwd="root")

dbcursor = mydb.cursor()
tbcursor = mydb.cursor()

def create_db():
    dbcursor.execute("""CREATE DATABASE IF NOT EXISTS pj
    CHARSET utf8 COLLATE utf8_general_ci""")

def create_table():
    tbcursor.execute("""SHOW DATABASES""")
for db in tbcursor:
    print(db)
