import psycopg2
#Create Database
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def condb():
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="0000")
    mydb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT); #Important to 'cannot run inside a transaction block'
    return mydb
# Connect DB
def condb_cloud():
    mydb = psycopg2.connect(
        host="ec2-35-170-123-64.compute-1.amazonaws.com",
        database="dcum35quhdj8v2",
        user="pjqjwoellzxpco",
        password="e45d24ff005b0ffa4590d3bcfc1ddb6ed92bcae4808215ebefe929e9ae14592b",
        port="5432")
    return mydb

