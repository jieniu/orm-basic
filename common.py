from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine


def getURL(user, passwd, host, port, database="", driver="mysql"):
    mysql_db = {'drivername': driver,
                'username': user,
                'password': passwd,
                'host': host,
                'port': port,
                'database': database}
    return URL(**mysql_db)


def createDatabase(user, passwd, host, port, db):
    db_uri = getURL(user, passwd, host, port)
    engine = create_engine(db_uri)
    engine.execute("create database if not exists %s" % db)

createDatabase("root", "", "localhost", 3306, "mydb")
