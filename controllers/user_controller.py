from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException
)
import sqlalchemy
from sqlalchemy.orm import Session
from starlette import status

from schemas.user import User
from database.tables.user import DBUser
from database.db_config import get_db


router = APIRouter(tags=["users"])


@router.get("/users")
async def index(db: Session = Depends(get_db)):
    return db.query(DBUser).all()


@router.get("/users/{user_id}")
async def show(user_id: int, db: Session = Depends(get_db)):
    user: DBUser | None = db.query(DBUser).filter(DBUser.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user


@router.post("/users")
async def create(user: User, db: Session = Depends(get_db)):
    new_user: DBUser = DBUser(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/users/{user_id}")
async def update(user_id: int, user: User, db: Session = Depends(get_db)):
    updated_user: DBUser | None = db.query(DBUser).filter(DBUser.id == user_id).first()

    if updated_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    db.execute(
        sqlalchemy.update(DBUser)
        .where(DBUser.id == user_id)
        .values(user.model_dump())
    )
    db.commit()
    db.refresh(updated_user)

    return updated_user


@router.delete("/users/{user_id}")
async def destroy(user_id: int, db: Session = Depends(get_db)):
    user_query = db.query(DBUser).filter(DBUser.id == user_id)

    if user_query.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    user_query.delete()
    db.commit()

    return status.HTTP_204_NO_CONTENT
