from sqlalchemy import VARCHAR, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    """
    Represents a row in the database
    Attributes:
        __tablename__: table name
        id: identification number of each row
        address: account address
        time: time when a request was completed
    """

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(VARCHAR(34))
    time: Mapped[datetime] = mapped_column(DateTime)
