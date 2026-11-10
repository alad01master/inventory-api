from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Product
from .schemas import ProductCreate, ProductResponse,ProductUpdate


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management API",
    version="1.0.1"
)


@app.get("/")
def home():
    return {
        "message": "Inventory API is running"
    }

#create new product

@app.post("/products",response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# read all

@app.get("/products", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):

    products = db.query(Product).all()

    return products

#read some 

@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

# update 

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):

    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product_data.name is not None:
        product.name = product_data.name

    if product_data.price is not None:
        product.price = product_data.price

    if product_data.quantity is not None:
        product.quantity = product_data.quantity

    db.commit()
    db.refresh(product)

    return product

# delete

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }