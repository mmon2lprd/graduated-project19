import psycopg2
#Create Database
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def createdb():
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="root")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT); #Important to 'cannot run inside a transaction block'
    cre = conn.cursor()
    #Check CREATE DATABASE IF EXISTS
    dbName = "vetdb"
    #pg_catalog.pg_database more https://www.postgresql.org/docs/current/catalog-pg-database.html
    cre.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname ='"+dbName+"';")
    exists = cre.fetchone()
    if not exists:
        cre.execute("CREATE DATABASE "+dbName+";")
        print('Create Database vetdb Successful!')
    else:
        print('Database vetdb is exists!')
    cre.close()
    conn.close()
    return False

# Connect DB
def condb():
    mydb = psycopg2.connect(
        host="localhost",
        database="vetdb",
        user="postgres",
        password="root")
    return mydb
