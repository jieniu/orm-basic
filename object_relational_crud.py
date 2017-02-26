import common
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer)

from sqlalchemy.orm import (
    mapper,
    scoped_session,
    sessionmaker)


class TableTemp(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age


def get_meta():
    db_url = common.getURL("root", "", "localhost", 3306, "mydb")
    engine = create_engine(db_url)
    return MetaData(engine, reflect=True), engine


def get_table(name, meta, engine):
    if name in meta.tables:
        table = meta.tables[name]
    else:
        table = Table(name, meta,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(255)),
                      Column('age', Integer))
        table.create(engine)

    cls = type(name.title(), (TableTemp,), {})
    mapper(cls, table)
    return cls

def get_session(engine):
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


# create
meta, engine = get_meta()
session = get_session(engine)
User = get_table("user", meta, engine)
try:
    row = User(name="Jerry", age=18)
    session.add(row)
    for res in session.query(User).all():
        print "add success: name(%s), age(%d)" % (res.name, res.age)
    session.commit()
except Exception as e:
    session.rollback()

# read
query = session.query(User).filter(User.name == 'Jerry')
for _row in query.all():
    print "query success: name(%s), age(%d)" % (res.name, res.age)

# update
try:
    row = session.query(User).filter(User.name == 'Jerry').first()
    row.age = 19
    session.commit()
except Exception as e:
    session.rollback()
finally:
    row = session.query(User).filter(User.name == 'Jerry').first()
    print "update success: name(%s), age(%d)" %(row.name, row.age)

# delete
query = session.query(User).filter(User.name=='Jerry')
query.delete()
session.commit()
query = session.query(User).filter(User.name=='Jerry')
print "delete success: %s" % query.all()

session.close()
