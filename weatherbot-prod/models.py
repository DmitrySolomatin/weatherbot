from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

Base= declarative_base()
engine = create_engine(os.getenv('APP_DATABASE_URL'))

class UserCoord(Base):
    __tablename__='usercoord'
    id=Column(Integer, primary_key=True)
    u_id=Column(Integer(),index=True)
    name=Column(String(60))
    lat=Column(String(16))
    lon=Column(String(16))

    def __repr__(self):
        return "<Coordinates(name='{}', lat='{}', lon='{}', u_id='{}')>".format(self.name,
                                                                                       self.lat, self.lon, self.u_id)

Base.metadata.create_all(engine)
