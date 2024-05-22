from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship
)
from database.db_config import Base
from . import item, user


class DBSale(Base):
    __tablename__ = "sale_tb"

    id: Mapped[int] = mapped_column(
        name="sale_id",
        primary_key=True,
        nullable=False,
        autoincrement="auto"
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_tb.user_id"),
        name="user_id",
        nullable=False
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item_tb.item_id"),
        name="item_id",
        nullable=False
    )
    user: Mapped["user.DBUser"] = relationship(back_populates="items")
    item: Mapped["item.DBItem"] = relationship(back_populates="users")
