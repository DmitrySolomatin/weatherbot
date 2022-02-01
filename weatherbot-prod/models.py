from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base= declarative_base()
engine = create_engine("postgresql://weather_admin:weather?@hostname/weather_bot")
class User(Base):
    __tablename__='userw'
    id = Column(Integer,primary_key=True )
    user_id_=Column(String)
    username=Column(String)

class Query(Base):
    __tablename__='queryw'
    id=Column(Integer, primary_key=True)
    #user=
    temp_ra=Column(Integer)
    feels_like= Column(Integer)
    description=Column(String)
    date=Column(Date)