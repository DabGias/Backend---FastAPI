from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException
)
import sqlalchemy
from sqlalchemy.orm import Session
from starlette import status

from database.db_config import get_db
from database.tables.item import DBItem
from database.tables.sale import DBSale
from schemas.sale import Sale


router = APIRouter(tags=["sales"])


@router.get("/sales/user/{user_id}")
async def show_user_sales(user_id: int, db: Session = Depends(get_db)):
    sales = db.query(DBItem).select_from(DBItem).where(DBSale.user_id == user_id).join(DBSale, DBSale.item_id == DBItem.id).all()

    if sales is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    return sales


@router.get("/sales")
async def index(db: Session = Depends(get_db)):
    return db.query(DBSale).all()


@router.get("/sales/{sale_id}")
async def show(sale_id: int, db: Session = Depends(get_db)):
    sale: DBSale | None = db.query(DBSale).filter(DBSale.id == sale_id).first()

    if sale is None:
        return HTTPException(status.HTTP_404_NOT_FOUND)
    
    return sale


@router.post("/sales")
async def create(sale: Sale, db: Session = Depends(get_db)):
    new_sale: DBSale = DBSale(**sale.model_dump())

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale
