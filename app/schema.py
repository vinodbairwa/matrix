from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


# ProductCategory Pydantic Models
class ProductCategoryCreate(BaseModel):
    base_category_name: str
    category_name: str
    description: Optional[str] = None
    starting_price: Optional[float] = 0
    is_recommended: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @validator("*", pre=True)
    def lowercase_strings(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value
    class Config:
        from_attributes = True


class ProductCategoryUpdate(BaseModel):
    base_category_name: Optional[str] = None
    category_name: Optional[str] = None
    description: Optional[str] = None
    starting_price: Optional[float] = None
    is_recommended: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProductCategoryResponse(ProductCategoryCreate):
        id: int

        class Config:
          from_attributes = True

# ------------ProductOption Pydantic Models----------------
class ProductOptionCreate(BaseModel):
    category_id: int
    tittle: str
    product_name: str
    description: Optional[str] = None
    is_recommended: Optional[bool] = False
    selection_type: Optional[str] = "Monthly"
    starting_price: Optional[float] = 0
    price: Optional[float] = 0
    offer_price: Optional[float] = 0
    icon: Optional[str] = None
    type: str
    max_deployment: Optional[int] = 0
    max_indicator_access: Optional[int] = 0
    max_signal_access: Optional[int] = 0
    max_brokers: Optional[int] = 0
    max_webhook_strategies: Optional[int] = 0
    max_alerts_per_day: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("*", pre=True)
    def lowercase_strings(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value
    
    class Config:
      from_attributes = True


class ProductOptionUpdate(BaseModel):
    category_id: Optional[int] = None
    tittle: Optional[str] = None
    product_name: Optional[str] = None
    description: Optional[str] = None
    is_recommended: Optional[bool] = None
    selection_type: Optional[str] = None
    starting_price: Optional[float] = None
    price: Optional[float] = None
    offer_price: Optional[float] = None
    icon: Optional[str] = None
    type: Optional[str] = None
    max_deployment: Optional[int] = None
    max_indicator_access: Optional[int] = None
    max_signal_access: Optional[int] = None
    max_brokers: Optional[int] = None
    max_webhook_strategies: Optional[int] = None
    max_alerts_per_day: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

   

#-------------------------------- ProductSubOption--------------------------------------
class ProductSubOptionBase(BaseModel):
    product_option_id: int
    sub_product_name: str
    description: Optional[str] = ""
    is_recommended: bool = False
    selection_type: str = ""  # Monthly, Quarterly, Yearly
    starting_price: float = 0
    price: float = 0
    icon: str = ""
    tag: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("*", pre=True)
    def lowercase_strings(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value

class ProductSubOptionCreate(ProductSubOptionBase):
        pass

  

class ProductSubOptionUpdate(ProductSubOptionBase):
    product_option_id: Optional[int] = None
    sub_product_name: Optional[str] = None
    description: Optional[str] = None
    is_recommended: Optional[bool] = None
    selection_type: Optional[str] = None
    starting_price: Optional[float] = None
    price: Optional[float] = None
    icon: Optional[str] = None
    tag: Optional[str] = None

class ProductSubOption(ProductSubOptionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
       from_attributes = True

# --------------------- FeaturesProduct ----------------------------------
class FeaturesProductBase(BaseModel):
    product_option_id: Optional[int]
    product_sub_option_id: int
    title: str = ""
    is_enable: bool = False
    products: str = ""

    @validator("*", pre=True)
    def lowercase_strings(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value

class FeaturesProductCreate(FeaturesProductBase):
    pass

class FeaturesProductUpdate(FeaturesProductBase):
    product_option_id: Optional[int] = None
    product_sub_option_id: Optional[int] = None
    title: Optional[str] = None
    is_enable: Optional[bool] = None
    products: Optional[str] = None

class FeaturesProduct(FeaturesProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
