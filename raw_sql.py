import common
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String


def testCreateTable(table_name):
    db_uri = common.getURL("root", "", "localhost", 3306, "mydb")
    engine = common.create_engine(db_uri)
    metadata = MetaData(engine)
    if not engine.dialect.has_table(engine, table_name):
        table = Table('EX1', metadata,
                      Column('id', Integer,
                             primary_key=True, autoincrement=True),
                      Column('name', String(255), nullable=False))
        table.create()


def testCRUD():
    db_uri = common.getURL("root", "", "localhost", 3306, "mydb")
    engine = common.create_engine(db_uri)

    # Create
    engine.execute('INSERT INTO EX1 '
                   '(name) '
                   'VALUES ("raw1")')

    # Read
    result = engine.execute('SELECT * FROM '
                            'EX1')
    for _r in result:
        print _r

    # Update
    engine.execute('UPDATE EX1 set name="raw" '
                   'WHERE name="raw1"')
    result = engine.execute('SELECT * FROM '
                            'EX1')
    print result.fetchall()

    # Delete
    engine.execute('DELETE from EX1 where name="raw"')
    result = engine.execute('SELECT * FROM EX1')
    print result.fetchall()


testCreateTable("EX1")
testCRUD()
