from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    CheckConstraint,
    Computed,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mssql import DATETIMEOFFSET

Base = declarative_base()


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    instrument = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    pnl = Column(Float, nullable=True)
    date = Column(DATETIMEOFFSET, nullable=False)
    strategy = Column(String, nullable=True)
    size = Column(Integer, nullable=False)
    fee = Column(Float, nullable=True)
    side = Column(String, nullable=False)
    amount = Column(Float, Computed("price * size"))

    # Add a check constraint to enforce "long" or "short" values for the side column
    __table_args__ = (
        CheckConstraint(side.in_(["long", "short"]), name="check_side_valid_values"),
    )


server = "GTX6060"  # As per the image
database = "backtest_db"  # Make sure this is the correct database name

# Use Windows Authentication with pyodbc
DATABASE_URL = f"mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
