import os

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker


from sql_connection import engine
from sql_maped_db import User, Expense, Income, Category
from auth import hash_password, verify_password, create_token

app = FastAPI()
SessionLocal = sessionmaker(bind=engine)


#schemas

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email:str
    password: str


#endpoints
#test get users query
@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [{"userid": u.userid, "username": u.username, "email": u.email} for u in users]
 
#allow a person to signup as a user
@app.post("/register")
def register(data: RegisterRequest):
    db = SessionLocal()
 
    # Check if email already exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
 
    # Find next available ID
    max_user = db.query(User).order_by(User.userid.desc()).first()
    next_id = (max_user.userid + 1) if max_user else 1
 
    # Create user with hashed password
    new_user = User(
        userid=next_id,
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(new_user)
    db.commit()
    db.close()
    return {"message": "Account created successfully"}
 
#get the user to login
@app.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
 
    user = db.query(User).filter(User.email == data.email).first()
    db.close()
 
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
 
    token = create_token({"sub": str(user.userid), "username": user.username})
    return {"token": token, "username": user.username}

#For DASHBOARD
#GET income
#GET Expenses
@app.get("/dashboard")
def get_dashboard(userid: int):
    db = SessionLocal()
#GET income
#display income total? not sure how i want to show it for now
    total_income = db.query(Income).filter(Income.userid == userid).all()
    income_sum = sum(i.amount for i in total_income)
#GET Expenses
    total_expenses = db.query(Expense).filter(Expense.userid == userid).all()
    expense_sum = sum(i.amount for i in total_expenses)

    db.close()

    return {"total_income": income_sum,
            "total_expenses": expense_sum,
            "balance": income_sum - expense_sum
        }





 
# serve /frontend, keep at end
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True), name="frontend")