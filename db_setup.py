from sqlalchemy import (
	Column,
	String,
	Integer,
	ForeignKey
	)
from sqlalchemy.orm import (
	relationship,backref
	)
from sqlalchemy.ext.declarative import(
	declarative_base	
	)
from sqlalchemy import create_engine
Base = declarative_base()

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer,primary_key=True)
	name = Column(String(100),nullable=False)
	email = Column(String(100),nullable=False)
	password = Column(String(25),nullable=False)

class Post(Base):
	__tablename__ = "posts"
	id = Column(Integer, primary_key= True)
	title = Column(String(500),nullable=False)
	image = Column(String(900),nullable=False)
	user_id = Column(Integer,ForeignKey('users.id'))
	user = relationship(User,backref='posts')

engine = create_engine('sqlite:///mydb.db')
Base.metadata.create_all(engine)
print('tables created successfully')


