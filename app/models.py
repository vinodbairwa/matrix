from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Double, ForeignKey, TIMESTAMP, Index
from sqlalchemy.orm import relationship
from .database import Base

import sqlalchemy as sa


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_category_name = Column(String(255), nullable=False)  # Matrix ONE, Matrix EDGE, Matrix ALGO
    category_name = Column(String(255), nullable=False)  #  webhook, indicator, signals,Screener
    description = Column(sa.Text, nullable=False, default="")
    starting_price = Column(Double, nullable=False, default=0)
    is_recommended = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("ProductOption", back_populates="category", cascade="all, delete-orphan")


class ProductOption(Base):
    __tablename__ = "product_options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)
    tittle = Column(String(255), nullable=False, default="")
    product_name = Column(String(255), nullable=False)
    description = Column(sa.Text, nullable=False, default="")
    is_recommended = Column(Boolean, nullable=False, default=False)
    selection_type = Column(String(255), nullable=False, default="")  # Monthly, Quarterly, Yearly
    starting_price = Column(Double, nullable=False, default=0)
    price = Column(Double, nullable=False, default=0)
    offer_price = Column(Double, nullable=False, default=0)
    icon = Column(String(255), nullable=False, default="")
    type = Column(String(255), nullable=False)  # public or private
    max_deployment = Column(Integer, nullable=False, default=0)
    max_indicator_access = Column(Integer, nullable=False, default=0)
    max_signal_access = Column(Integer, nullable=False, default=0)
    max_brokers = Column(Integer, nullable=False, default=0)
    max_webhook_strategies = Column(Integer, nullable=False, default=0)
    max_alerts_per_day = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("ProductCategory", back_populates="products")
    
    sub_category = relationship("ProductSubOption", back_populates="Product_Option")


    
class ProductSubOption(Base):
    __tablename__ = "product_sub_options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_option_id = Column(Integer, ForeignKey("product_options.id"), nullable=False)
    sub_product_name = Column(String(255), nullable=False)
    description = Column(sa.Text, nullable=False, default="")
    is_recommended = Column(Boolean, nullable=False, default=False)
    selection_type = Column(String(255), nullable=False, default="")  # Monthly, Quarterly, Yearly
    starting_price = Column(Double, nullable=False, default=0)
    price = Column(Double, nullable=False, default=0)
    icon = Column(String(255), nullable=False, default="")
    tag = Column(String(255), nullable=False, default="")
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Product_Option = relationship("ProductOption", back_populates="sub_category", cascade="all, delete-orphan")
    Product_Option = relationship("ProductOption", back_populates="sub_category")
  
class FeaturesProduct(Base):
    __tablename__ = "features_product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_option_id = Column(Integer, ForeignKey("product_options.id"), nullable=False)  # Foreign key to product_options
    product_sub_option_id = Column(Integer, ForeignKey("product_sub_options.id"), nullable=False)  # Foreign key to product_sub_options
    title = Column(String(255), nullable=False, default="")  # Corrected 'tittle' to 'title'
    is_enable = Column(Boolean, nullable=False, default=False)
    products = Column(String(255), nullable=False, default="")
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Define relationships
    product_option = relationship("ProductOption", backref="features_products")
    product_sub_option = relationship("ProductSubOption", backref="features_products")

    # Create appropriate indexes for the foreign keys
    __table_args__ = (
        Index("idx_product_option_id", "product_option_id"),
        Index("idx_product_sub_option_id", "product_sub_option_id"),
    )

