from datetime import date
from datetime import date, time
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
import models

app = FastAPI()

class Product(BaseModel):
    id:Optional[int]
    name:str
    price_to:float
    image:str
    department:str
    category:str
    store:str
    available:str
    created_at:Optional[date]
    hour:Optional[time]
    
    class Config:
        orm_mode=True

db = SessionLocal()

@app.get('/products', response_model=List[Product], status_code=status.HTTP_200_OK)
def get_all_products():
    items = db.query(models.Product).all()
    return items

@app.get('/product/{id}', response_model=Product, status_code=status.HTTP_200_OK)
def get_a_product(id: int):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    
    return product

@app.post('/products', response_model=Product, status_code=status.HTTP_201_CREATED)
def create_a_product(product: Product):
    new_product = models.Product(
        name = product.name,
        price_to = product.price_to,
        image = product.image,
        department = product.department,
        category = product.category,
        store = product.store,
        available = product.available,
        created_at = product.created_at,
        hour = product.hour
    )
    
    #db_item = db.query(models.Product).filter(product.name == new_product.name).first()
    
    #if db_item is not None:
    #    raise HTTPException(status_code=400, detail= "Produto já existe na base de dados")
    
    db.add(new_product)
    
    try:
        db.commit()
    except:
        db.rollback()
        raise
    #finally:
    #    db.close()
    
    return new_product

@app.delete('/product/{id}')
def delete_product(id: int):
    product_to_delete = db.query(models.Product).filter(models.Product.id == id).first()
    
    if product_to_delete is None:
        raise HTTPException(statuscode=status.HTTP_404_NOT_FOUND, detail="Produto inexistente na base de dados")
    
    return product_to_delete