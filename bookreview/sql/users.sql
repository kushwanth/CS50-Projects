CREATE TABLE users(
username VARCHAR PRIMARY KEY,
email VARCHAR CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
password VARCHAR not null);
