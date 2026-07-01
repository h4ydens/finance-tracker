from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    #columns
    userid = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(225), unique=True, nullable=False)
    password_hash = Column(String(225), unique=True, nullable=False)
    
    #realations to query faster
    incomes = relationship("Income", back_populates="user")
    expenses = relationship("Expense", back_populates="user")


class Income(Base):
    __tablename__ = "income"

    #columns
    incomeid = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    date_received = Column(Date)
    description = Column(String(225))

    #fk
    userid = Column(Integer, ForeignKey("users.userid"))

    #realations to query faster
    user = relationship("User", back_populates="incomes")



class Category(Base):
    __tablename__ = "categories"

    #columns
    categoryid = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)

    #realations to query faster
    expenses = relationship("Expense", back_populates="category")



class Expense(Base):
    __tablename__ = "expenses"

    #columns
    expenseid = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    date_spent = Column(Date, nullable=False)
    description = Column(String(225))

    #fk
    userid = Column(Integer, ForeignKey("users.userid"))
    categoryid = Column(Integer, ForeignKey("categories.categoryid"))

    #realations to query faster
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")