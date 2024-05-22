from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException
)
import sqlalchemy
from sqlalchemy.orm import Session
from starlette import status

from schemas.item import Item
from database.tables.item import DBItem
from database.db_config import get_db


router = APIRouter(tags=["items"])


@router.get("/items")
async def index(db: Session=Depends(get_db)):
    return db.query(DBItem).all()


@router.get("/items/{item_id}")
async def show(item_id: int, db: Session = Depends(get_db)):
    item: DBItem | None = db.query(DBItem).filter(DBItem.id == item_id).first()

    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return item


@router.post("/items")
async def create(item: Item, db: Session = Depends(get_db)):
    new_item: DBItem = DBItem(**item.model_dump())
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.put("/items/{item_id}")
async def update(item_id: int, item: Item, db: Session = Depends(get_db)):
    updated_item: DBItem | None = db.query(DBItem).filter(DBItem.id == item_id).first()
    
    if updated_item is None:
        return HTTPException(status.HTTP_404_NOT_FOUND)
    
    db.execute(
        sqlalchemy.update(DBItem)
        .where(DBItem.id == item_id)
        .values(item.model_dump())
    ) 
    db.commit()
    db.refresh(updated_item)

    return updated_item


@router.delete("/items/{item_id}")
async def destroy(item_id: int, db: Session = Depends(get_db)):
    item_query = db.query(DBItem).filter(DBItem.id == item_id)

    if item_query.first() is None:
        return HTTPException(status.HTTP_404_NOT_FOUND)
    
    item_query.delete()
    db.commit()

    return status.HTTP_204_NO_CONTENT
