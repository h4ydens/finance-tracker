from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    #columns
    userID = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(225), unique=True, nullable=False)
    password_hash = Column(String(225), unique=True, nullable=False)
    
    #realations to query faster
    incomes = relationship("income", back_populates="user")
    expenses = relationship("expenses", back_populates="user")


class Income(Base):
    __tablename__ = "income"

    #columns
    incomeID = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    date_recived = Column(Date)
    description = Column(String(225))

    #fk
    userID = Column(Integer, ForeignKey("users.userID"))

    #realations to query faster
    user = relationship("User", back_populates="incomes")



class Category(Base):
    __tablename__ = "categories"

    #columns
    categoryID = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)

    #realations to query faster
    expenses = relationship("Expense", back_populates="category")



class Expense(Base):
    __tablename__ = "expenses"

    #columns
    expenseID = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    date_spent = Column(Date, nullable=False)
    description = Column(String(225))

    #fk
    userID = Column(Integer, ForeignKey("users.userID"))
    CategoryID = Column(Integer, ForeignKey("categories.categoryID"))

    #realations to query faster
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")