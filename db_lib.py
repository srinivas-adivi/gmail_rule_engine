from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Define email model
class Message(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    msg_id = Column(String, unique=True)
    sender = Column(String)
    receiver = Column(String)
    subject = Column(String)
    body = Column(String)
    received_date = Column(DateTime)

engine = create_engine('sqlite:///emails.db')
Session = sessionmaker(bind=engine)
session = Session()
