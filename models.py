from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Float
from database import Base


class freq(Base):
    __tablename__ = 'frequency'
    id = Column(Integer,primary_key=True, index=True)
    freq = Column(Float)
    institution = Column(String)
    usage = Column(String)



