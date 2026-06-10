CREATE TABLE users (
userID int PRIMARY KEY,
username varchar(25) UNIQUE NOT NULL,
email varchar(100) UNIQUE NOT NULL,
password varchar(25) NOT NULL
);

