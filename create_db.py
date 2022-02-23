from database import Base, engine
from models import Product

print("Criando base de dados...")

Base.metadata.create_all(engine)