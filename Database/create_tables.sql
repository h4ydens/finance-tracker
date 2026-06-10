CREATE TABLE Users (
	userID int PRIMARY KEY,
	username varchar(25) UNIQUE NOT NULL,
	email varchar(225) UNIQUE NOT NULL,
	password_hash varchar(225) NOT NULL
);

CREATE TABLE Income (
	incomeID int Primary KEY,
	amount int NOT NULL,
	date_received DATE,
	description varchar(225),
	userID int,
	CONSTRAINT fk_users
		FOREIGN KEY (UserID)
		REFERENCES Users(userID) 
);

CREATE TABLE Categories (
	categoryID int Primary KEY,
	category_name varchar(100) NOT NULL
);

CREATE TABLE Expenses (
	expenseID int Primary KEY,
	amount int NOT NULL,
	date_spent DATE NOT NULL,
	description varchar(225),

	userID INT,
    categoryID INT,

    CONSTRAINT fk_expense_user
        FOREIGN KEY (userID)
        REFERENCES Users(userID),

    CONSTRAINT fk_expense_category
        FOREIGN KEY (categoryID)
        REFERENCES Categories(categoryID)
);
