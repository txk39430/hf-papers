from sqlalchemy import String, Integer, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    authors: Mapped[str | None] = mapped_column(Text, nullable=True)
    published: Mapped[Date | None] = mapped_column(Date, nullable=True)
    url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)

