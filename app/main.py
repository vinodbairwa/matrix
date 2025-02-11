from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Dict
from datetime import datetime

from app.models import FeaturesProduct, ProductCategory, ProductOption, ProductSubOption
from app.schema import FeaturesProductCreate, FeaturesProductUpdate, ProductCategoryCreate,  ProductCategoryUpdate, ProductOptionCreate, ProductOptionUpdate, ProductSubOptionCreate, ProductSubOptionUpdate
from .database import*
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # or specify frontend domain like ["http://localhost:3000"]
    allow_credentials=True,  # Ensure credentials are allowed
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
   
)
# ---------------Helper function to update the fields----------
def update_instance(instance, data: Dict):
    for key, value in data.items():
        if value is not None:
            setattr(instance, key, value)


# ----------------------Create Product Category----------------
@app.post("/product_categories/create/")
async def create_product_category(data: ProductCategoryCreate,  db: Session=Depends(get_db)):
    try:
        new_category = ProductCategory(**data.dict())

        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return {"message": f"Product category {new_category.base_category_name} created successfully!"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# -----------------Update Product Category-------------------------
@app.put("/product_categories/update/{category_id}")
async def update_product_category(category_id: int, data: ProductCategoryUpdate,  db: Session=Depends(get_db)):
    try:
        category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Product category not found")

        update_instance(category, data.dict())  # using the helper function
        category.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(category)
        return {"message": f"Product category {category_id} updated successfully!","data":category}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the category")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# -----------------Delete Product Category-------------------------
@app.delete("/product_categories/delete/{category_id}")
async def delete_product_category(category_id: int, db: Session=Depends(get_db)):
    try:
        category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Product category not found")
            
        db.delete(category)
        db.commit()
        db.refresh(category)
        return {"message": f"Product category {category_id} deleted successfully!","data":category}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the category")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# -----------------Get Product Category-------------------------
@app.get("/product_categories/get/")
async def get_product_category(db: Session=Depends(get_db),category_id: int = Query(None, alias="category_id")):
    try:
        if category_id is not None:
            category = db.query(ProductCategory).filter(ProductCategory.id ==category_id).all()
        
            if not category:
                raise HTTPException(status_code=404, detail="Product category not found")
            return {"message": f"Product category {category_id} fatch data successfully!","data":category}
        else:
            category = db.query(ProductCategory).all()
            if not category:
                raise HTTPException(status_code=404, detail="Product category not found")
            return {"message": f"Product category {category_id} fatch data successfully!","data":category}
            
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the category")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")




#_____________________________________________________________________________________________________________________________
# ------------------Create Product Option-------------------
@app.post("/product_options/create/")
async def create_product_option(data: ProductOptionCreate,  db: Session=Depends(get_db)):
    try:
        new_option = ProductOption(**data.dict())

        db.add(new_option)
        db.commit()
        db.refresh(new_option)
        return {"message": f"Product option {new_option.product_name} created successfully!"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Option already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# ---------------------Update Product Option-------------------
@app.put("/product_options/Update/{option_id}")
async def update_product_option(option_id: int, data: ProductOptionUpdate,  db: Session=Depends(get_db)):
    try:
        option = db.query(ProductOption).filter(ProductOption.id == option_id).first()
        if not option:
            raise HTTPException(status_code=404, detail="Product option not found")

        update_instance(option, data.dict())  # using the helper function
        option.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(option)
        return {"message": f"Product option {option_id} updated successfully!","data":option}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the option")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# ---------------------Delete Product Option-------------------
@app.delete("/product_options/delete/{option_id}")
async def update_product_option(option_id: int,  db: Session=Depends(get_db)):
    try:
        option = db.query(ProductOption).filter(ProductOption.id == option_id).first()
        if not option:
            raise HTTPException(status_code=404, detail="Product option not found")

        db.delete(option)
        db.commit()
        return {"message": f"Product option {option_id} deleted successfully!","data":option}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the option")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# ---------------------Get Product Option-------------------
@app.get("/product_options/get/")
async def update_product_option(db: Session=Depends(get_db),option_id=Query(None)):
    try:
        if option_id:
            option = db.query(ProductOption).filter(ProductOption.id == option_id).first()
            if not option:
                raise HTTPException(status_code=404, detail="Product option not found")
            return {"message": f"Product option {option} fetch data successfully!","data":option}
        else:
            option = db.query(ProductOption).all()
            if not option:
                raise HTTPException(status_code=404, detail="Product not found")
            return {"message": f"Product fetch data successfully!","data":option}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the option")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# ____________________________________________________________________

# ------------------Create Product sub Option-------------------
@app.post("/product_sub_options/create/")
async def create_product_option(data: ProductSubOptionCreate,  db: Session=Depends(get_db)):
    try:
        new_option = ProductSubOption(**data.dict())

        db.add(new_option)
        db.commit()
        db.refresh(new_option)
        return {"message": f"Product_sub_ option {new_option.sub_product_name} created successfully!"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Option already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


#----------------------------product_sub_options--------------------------

@app.put("/product_sub_options/update/{option_id}")
async def update_product_option(option_id: int, data: ProductSubOptionUpdate,  db: Session=Depends(get_db)):
    try:
        option = db.query(ProductSubOption).filter(ProductSubOption.id == option_id).first()
        if not option:
            raise HTTPException(status_code=404, detail="Product option not found")

        update_instance(option, data.dict())  # using the helper function
        option.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(option)
        return {"message": f"Product Sub option {option_id} updated successfully!","data":option}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the option")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



# ---------------------Delete Product subOption-------------------
@app.delete("/product_sub_options/delete/{option_id}")
async def update_product_option(option_id: int,  db: Session=Depends(get_db)):
    try:
        option = db.query(ProductSubOption).filter(ProductSubOption.id == option_id).first()
        if not option:
            raise HTTPException(status_code=404, detail="Product option not found")

        db.delete(option)
        db.commit()
        return {"message": f"Product_sub_option {option_id} deleted successfully!","data":option}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the option")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# ---------------------Get Product_SUb_Option-------------------
@app.get("/product_sub_options/get/")
async def update_product_option(db: Session=Depends(get_db),option_id=Query(None)):
    try:
        if option_id:
            option = db.query(ProductSubOption).filter(ProductSubOption.id == option_id).first()
            if not option:
                raise HTTPException(status_code=404, detail="Product option not found")
            return {"message": f"Product option {option} fetch data successfully!","data":option}
        else:
            option = db.query(ProductSubOption).all()
            if not option:
                raise HTTPException(status_code=404, detail="Product not found")
            return {"message": f"Product_sub_optional fetch data successfully!","data":option}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the option")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



# ____________________________________________________________________

# ------------------Create Pfeatures_product-------------------

@app.post("/features_product/create/")
async def create_product_option(data: FeaturesProductCreate,  db: Session=Depends(get_db)):
    try:
        new_option = FeaturesProduct(**data.dict())

        db.add(new_option)
        db.commit()
        db.refresh(new_option)
        return {"message": f"Feature option {new_option.products} created successfully!"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Option already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# ------------------Update features_product-------------------

@app.put("/features_product/update/{option_id}")
async def update_product_option(option_id: int, data: FeaturesProductUpdate,  db: Session=Depends(get_db)):
    try:
        option = db.query(FeaturesProduct).filter(FeaturesProduct.id == option_id).first()
        if not option:
            raise HTTPException(status_code=404, detail="Product option not found")

        update_instance(option, data.dict())  # using the helper function
        option.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(option)
        return {"message": f"Feature option {option_id} updated successfully!","data":option}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the option")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



# ------------------Delete features_product-------------------

@app.delete("/features_product/delete/{option_id}")
async def update_product_option(option_id: int, db: Session=Depends(get_db)):
    try:
        option = db.query(FeaturesProduct).filter(FeaturesProduct.id == option_id).first()
        if not option:
            raise HTTPException(status_code=404, detail="Product option not found")

        db.delete(option)
        db.commit()
        
        return {"message": f"Feature option {option_id} updated successfully!","data":option}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the option")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



# ---------------------Get Product_SUb_Option-------------------
@app.get("/features_product/get/")
async def update_product_option(db: Session=Depends(get_db),option_id=Query(None)):
    try:
        if option_id:
            option = db.query(FeaturesProduct).filter(FeaturesProduct.id == option_id).first()
            if not option:
                raise HTTPException(status_code=404, detail="Product option not found")
            return {"message": f"Features Product {option} fetch data successfully!","data":option}
        else:
            option = db.query(FeaturesProduct).all()
            if not option:
                raise HTTPException(status_code=404, detail="Product not found")
            return {"message": f"FeaturesProduct fetch data successfully!","data":option}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating the option")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

