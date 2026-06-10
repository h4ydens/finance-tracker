from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sql_connection import engine
from sql_maped_db import User, Expense, Income, Category

app = FastAPI()
sessionLocal = sessionmaker(bind=engine)

@app.get("/users")

def get_users():
    db = sessionLocal()
    users = db.query(User).all()
    return users