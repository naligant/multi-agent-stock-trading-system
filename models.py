from pydantic import BaseModel
from typing import Optional
import sqlite3

# Database setup
DATABASE_URL = "stock_data.db" # Use a constant

#make sql connection for database
def create_connection():
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    return conn

#create the database table
def market_data_create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            date TEXT,
            open DOUBLE,
            high DOUBLE,
            low DOUBLE,
            close DOUBLE,
            dividends DOUBLE,
            stock_splits DOUBLE
        )
    """)
    conn.commit()

def news_data_create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news_data (
        date DATE PRIMARY KEY,
        headline TEXT,
        summary TEXT
    )
""")

# Pydantic models
#the input for the stock data
class MarketDataCreate(BaseModel):
    ticker: str
    date: str  # or datetime if you want to parse it
    open: float
    high: float
    low: float
    close: float
    volume: int
    dividends: float
    stock_splits: float

# class TaskCreate(BaseModel):
#     user_input: str

class NewsDataCreate(BaseModel):
    date: str
    headline: str
    summary: str
    
class TaskResponse(BaseModel):
    #id is optional so that it can be created when a task is made
    id: Optional[int] = None 
    ticker: str
    date: str  # or datetime if you want to parse it
    open: float
    high: float
    low: float
    close: float
    volume: int
    dividends: float
    stock_splits: float
