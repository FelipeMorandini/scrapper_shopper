from datetime import datetime
from database import Base
from sqlalchemy import Date, String, Integer, Float, Column, Time
from datetime import date, time

class Product(Base):
    __tablename__="products"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    price_to = Column(Float, nullable=False)
    image = Column(String(255), nullable=True)
    department = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    store = Column(String(255), nullable=False)
    available = Column(String(255), nullable=False)
    created_at = Column(Date(), default=date.today())
    hour = Column(Time(timezone=True), default=datetime.now().time())
    
    def __repr__(self):
        return f"<Product name={self.name} price_to={self.price_to}>"