from typing import List
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship
)
from . import sale
from database.db_config import Base


class DBItem(Base):
    __tablename__ = "item_tb"

    id: Mapped[int] = mapped_column(
        name="item_id",
        primary_key=True,
        nullable=False,
        autoincrement="auto"
    )
    name: Mapped[str] = mapped_column(
        name="item_name",
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        name="item_description",
        nullable=True
    )
    price: Mapped[float] = mapped_column(
        name="item_price",
        nullable=False
    )
    tax: Mapped[float] = mapped_column(
        name="item_tax",
        nullable=True
    )
    users: Mapped[List["sale.DBSale"]] = relationship(
        back_populates="item",
        cascade="merge"
    )
