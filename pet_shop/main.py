from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import engine, get_db

# Создаем таблицы при запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pet Shop API")


@app.post("/products", response_model=schemas.ProductResponse)
def create_item(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Проверка на уникальность имени
    existing = db.query(models.Product).filter(models.Product.name == product.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product name already registered")
    return crud.create_product(db=db, product=product)


@app.get("/products", response_model=List[schemas.ProductResponse])
def read_items(
        min_price: float = Query(None, ge=0),
        max_price: float = Query(None, ge=0),
        in_stock: bool = None,
        db: Session = Depends(get_db)
):
    if min_price and max_price and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price must be <= max_price")
    return crud.get_products(db, min_price, max_price, in_stock)


@app.get("/products/{id}", response_model=schemas.ProductResponse)
def read_item(id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put("/products/{id}", response_model=schemas.ProductResponse)
def update_item(id: int, product_data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Проверка уникальности имени при смене
    name_check = db.query(models.Product).filter(
        models.Product.name == product_data.name,
        models.Product.id != id
    ).first()
    if name_check:
        raise HTTPException(status_code=400, detail="Name already taken")

    return crud.update_product(db, db_product, product_data)


@app.delete("/products/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Success deleted"}