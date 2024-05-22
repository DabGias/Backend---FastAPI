from typing import List
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship
)
from . import sale
from database.db_config import Base


class DBUser(Base):
    __tablename__ = "user_tb"

    id: Mapped[int] = mapped_column(
        name="user_id",
        primary_key=True,
        nullable=False,
        autoincrement="auto"
    )
    email: Mapped[str] = mapped_column(
        name="user_email",
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        name="user_password",
        nullable=False
    )
    items: Mapped[List["sale.DBSale"]] = relationship(
        back_populates="user",
        cascade="merge"
    )
