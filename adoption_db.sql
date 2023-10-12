CREATE DATABASE adoption;
USE adoption;

CREATE TABLE customers (
    id   VARCHAR(255) NOT NULL PRIMARY KEY,
    firstname   VARCHAR(255),
    lastname    VARCHAR(255),
    phone 	VARCHAR(25),
    email	VARCHAR(255),
    address     VARCHAR(255),
    city_name    VARCHAR(255),
    state       VARCHAR(255),
    zipCode     VARCHAR(255),
    CreatedAt    DATETIME DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE customer_adoptions(
    pet_id INT NOT NULL PRIMARY KEY,
    customer_id VARCHAR(255),
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);


