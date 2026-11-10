from sqlalchemy import String, Numeric, Integer,DateTime,func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .database import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price_sen: Mapped[float] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)