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
def condb(ex):
    mydb = psycopg2.connect(
        host="ec2-3-89-0-52.compute-1.amazonaws.com",
        database="dedf80glcmk22j",
        user="fakonaqptkmunv",
        password="f4a3d92b09c7d1fe30b89ac80da037ee4015f05dc63212c4372847d37114ccb5")
    if(mydb):
        print('Connect database Successful!')
    if (ex==0):
        mydb.close()
        print('Disconnect database Successful!')
    return mydb
