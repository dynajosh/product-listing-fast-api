from fastapi import FastAPI, Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from db.models import Discount, Product, Base
from db.session import get_db, engine, populate_db
from db.schemas import DiscountSchema
from typing import List
from fastapi import HTTPException, status


def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

def start_application():
    app_instance=FastAPI()
    create_tables()
    # populate_db()
    return app_instance

app = start_application()


def create_discount(discount:DiscountSchema, db:Session):
    new_discount =Discount(
        sku=discount.sku,
        category=discount.category,
        percentage=discount.percentage
    )
    if discount.sku is None and discount.category is None:
        return "Please enter a sku or category"
    
    if new_discount.percentage is None:
        return "Please enter a value for percentage"

    print("adding new discount")

    try:
        db.add(new_discount)
        db.commit()
        db.refresh(new_discount)
        return new_discount
    except :
        raise HTTPException(status_code=409, detail="A discount for this product or category has already been created.")

 

def get_product_discount(product, db):

    sku_discount = db.query(Discount).filter(Discount.sku==product.sku).first()
    category_discount = db.query(Discount).filter(Discount.category==product.category).first()

    if sku_discount is not None and category_discount is not None:
        return max(sku_discount.percentage, category_discount.percentage)
    elif sku_discount is not None:
        return sku_discount.percentage
    elif category_discount is not None:
        return category_discount.percentage
    else:
        return None



@app.get("/")
async def index():
    return {
        "message" : "Inventory home"
    }

@app.get("/products")
async def list_products(category:str=None, price_less_than_or_equal_to:float=None, db:Session=Depends(get_db)):
    products = db.query(Product).all()
    if category:
        products = db.query(Product).filter(Product.category==category).all()
        print(products)

    if price_less_than_or_equal_to:
        products = db.query(Product).filter(Product.price <=price_less_than_or_equal_to).all()

    if category and price_less_than_or_equal_to:
        products = db.query(Product).filter(Product.price <=price_less_than_or_equal_to, Product.category==category).all()

    extra_data = {"active": True, "created_at": "2022-12-01T10:00:00"}

    products_list = []
    for product in products:
        applicable_discount = get_product_discount(product=product, db=db)
        # print(applicable_discount)

        if applicable_discount:
            price = {
                'original': product.price,
                'final': product.price * (1-(applicable_discount/100)),
                'currency': 'USD',
                'discount_percentage':str(applicable_discount)+"%"
            }
            products_list.append({
                'sku':product.sku,
                'name':product.name,
                'category':product.category,
                'price':price,
            })

        else :
            price = {
                'original': product.price,
                'final': product.price,
                'currency': 'USD',
                'discount_percentage':applicable_discount
            }
            products_list.append({
                'sku':product.sku,
                'name':product.name,
                'category':product.category,
                'price':price
            })


    return products_list


@app.post('/discount', response_model=DiscountSchema,)
async def add_discount(discount:DiscountSchema, db:Session = Depends(get_db)):
    discount = create_discount(discount=discount, db=db)
    return "Discount applied"