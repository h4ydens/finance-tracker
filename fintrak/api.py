import os

from datetime import date

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker


from sql_connection import engine
from sql_maped_db import User, Expense, Income, Category
from auth import hash_password, verify_password, create_token, decode_token

app = FastAPI()
SessionLocal = sessionmaker(bind=engine)

#auto formats the incoming Authorization: Bearer <token> header from incoming requests
security = HTTPBearer()


#schemas, needed for post

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email:str
    password: str

class ExpenseRequest(BaseModel):
    amount:int
    date_spent:date
    description:str
    categoryid:int

class IncomeRequest(BaseModel):
    amount:int
    date_received:date
    description:str

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
 
    #IMPORTENT TOKEN IS MADE HERE FOR USER
    #user id is under "sub"
    token = create_token({"sub": str(user.userid), "username": user.username})
    return {"token": token, "username": user.username}

#For DASHBOARD
#GET income
#GET Expenses
@app.get("/dashboard")
def get_dashboard(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_data = decode_token(credentials.credentials)
    userid = int(token_data["sub"])

    db = SessionLocal()

    #GET USER NAME, token gives username
    username = token_data["username"]

    #GET income
    #display income total? not sure how i want to show it for now
    total_income = db.query(Income).filter(Income.userid == userid).all()
    income_sum = sum(i.amount for i in total_income)
    #GET Expenses
    total_expenses = db.query(Expense).filter(Expense.userid == userid).all()
    expense_sum = sum(j.amount for j in total_expenses)

    today = date.today()
    #weird ass logic to get the data entry dates of 1 motnh
    this_month = db.query(Expense).filter(Expense.userid == userid, Expense.date_spent >= date(today.year, today.month, 1)).all()
    this_month_sum = sum(e.amount for e in this_month)

    #show the history of expenses in bottom tab
    recent = db.query(Expense).filter(Expense.userid == userid).order_by(Expense.date_spent.desc()).limit(5).all()
    recent_list = [
        {
            "amount": e.amount,
            "description": e.description,
            "date": str(e.date_spent)
        }
        for e in recent
    ]

    db.close()

    return {"total_income": income_sum,
            "total_expenses": expense_sum,
            "balance": income_sum - expense_sum,
            "this_month": this_month_sum,
            "recent_transactions": recent_list,
            "username": username
        }

#2 post and get apis for income and expenses
#need to be able to enter and retrieve users expenses
@app.post("/expenses")
def create_expenses(data: ExpenseRequest, credentials:HTTPAuthorizationCredentials = Depends(security)):
    token_data = decode_token(credentials.credentials)
    userid = int(token_data["sub"])

    db = SessionLocal()

    max_expense = db.query(Expense).order_by(Expense.expenseid.desc()).first()
    next_id = (max_expense.expenseid + 1) if max_expense else 1

    new_expense = Expense(
        expenseid = next_id,
        amount = data.amount,
        date_spent = data.date_spent,
        description = data.description,
        categoryid = data.categoryid,
        userid = userid
    )
    db.add(new_expense)
    db.commit()
    db.close()

    return {"message": "Expense added successfully"}

@app.get("/expenses")
def get_expenses(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_data = decode_token(credentials.credentials)
    userid = int(token_data["sub"])

    db = SessionLocal()

    #qury ts
    expenses = db.query(Expense).filter(Expense.userid == userid).order_by(Expense.date_spent.desc()).all()
    db.close()

    #return gucha
    return [
        {
            "expenseid": e.expenseid,
            "amount": e.amount,
            "date_spent": str(e.date_spent),
            "description": e.description,
            "categoryid": e.categoryid
        }
        for e in expenses
    ]

#need to be able to enter and retrieve users income
@app.post("/income")
def create_income(data: IncomeRequest, credentials:HTTPAuthorizationCredentials = Depends(security)):
    token_data = decode_token(credentials.credentials)
    userid = int(token_data["sub"])

    db = SessionLocal()
    #get latest id number
    max_income = db.query(Income).order_by(Income.incomeid.desc()).first()
    next_id = (max_income.incomeid + 1) if max_income else 1
    #post the entry
    new_income = Income(
            incomeid = next_id,
            amount = data.amount,
            date_received = data.date_received,
            description = data.description,
            userid = userid
    )
    db.add(new_income)
    db.commit()
    db.close()

    return {"message": "Income added successfully"}


@app.get("/income")
def get_income(credentials:HTTPAuthorizationCredentials = Depends(security)):
    token_data = decode_token(credentials.credentials)
    userid = int(token_data["sub"])

    db = SessionLocal()
    #get income userid 
    income = db.query(Income).filter(Income.userid == userid).order_by(Income.date_received.desc()).all()
    db.close()


    #return massive list
    return [
        {
            "incomeid": i.incomeid,
            "amount": i.amount,
            "date_received": str(i.date_received),
            "description": i.description
        }
        for i in income
    ]




# serve /frontend, keep at end
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True), name="frontend")