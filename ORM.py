#encoding=utf8
from sqlalchemy import Column, String, create_engine, Integer,BigInteger, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
Base = declarative_base()


class wehome(Base):
    __tablename__ = 'interview_wehome'

    room = Column(String(32), primary_key=True)
    location = Column(String(100))
    model = Column(String(32))
    roomer = Column(String(32))
    apartment = Column(String(32))
    bed = Column(String(32))


