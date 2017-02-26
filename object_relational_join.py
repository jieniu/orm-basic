from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    addresses = relationship("Address", backref="profile")


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    user_id = Column(Integer, ForeignKey('profile.id'))

db_url = {'drivername': 'mysql',
          'username': 'root',
          'password': '',
          'host': 'localhost',
          'port': 3306,
          'database': 'mydb'}

# create engine
engine = create_engine(URL(**db_url))

# create tables
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

profile = Profile(name='user1')
mail1 = Address(email='user1@foo.com')
mail2 = Address(email='user1@bar.com')
profile.addresses.extend([mail1, mail2])

session.add(profile)
session.add_all([mail1, mail2])
session.commit()

r = session.query(Address, Profile).join(Profile)
for _a, _u in r.all():
    print _u.name, _a.email
