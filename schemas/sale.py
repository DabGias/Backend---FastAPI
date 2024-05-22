from pydantic import BaseModel


class Sale(BaseModel):
    user_id: int
    item_id: int

    class Config:
        orm_mode = True
