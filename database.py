from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:1234@localhost/shopper",
    echo=True
)

Base=declarative_base()

SessionLocal = sessionmaker(bind=engine)