from pydantic import BaseModel,Field
from typing import List,Optional,Union


class ProductSchema(BaseModel):
    sku: str
    name: str
    category: str
    price:Optional[float]
    discount_percentage = float
    
    class Config:
        orm_mode = True
        

class DiscountSchema(BaseModel):
    sku: Optional[str] = None
    category:Optional[str] = None
    percentage:float=None

    class Config:
        orm_mode = True