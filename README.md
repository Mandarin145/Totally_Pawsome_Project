# cfg-project-group1
This application is a Python Flask web app that uses Jinja templates and SQLAlchemy to create a website which enables users to search through web api of pets available for adoption and adopt a pet of their preference. 



# Key Functionality
- Searching for a pet by filtering your criteria
- Looking through the list of pets available for adoption after filtering 
- It prioritises senior animals so the user will see these animals first if they are available after filtering.  
- Register to adopt a pet 
- This registration is now submitted to the database and the same pet can not be requested to be adopted again
- A user can also adopt many pets

# Download Code

Clone this repository via this link:


# Setup
Open MySQL Workbench and create a new database, called adoption.
Please create the database available in the *adoption_db.sql* file.
Run this file in your MySQL workbench to create the database and tables

```sql
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
```

Change the name of the *.env.example* to *.env* file (remove'.example') to connect your database to python and the web api used in this program.
In that file, please substitute 'yourusername' and 'yourpassword' for your personal username and password for your mysql database.


```python

DATABASE_USER=yourusername
DATABASE_PASSWORD=yourpassword
```

## Installing Requirements
Run this command in your terminal to install the necessary requirements for the programme

``` pip3 install -r requirements.txt ```

## Run
To start the Flask app, run *main.py* to start the program and click on the http link that generates in your console for it to appear on your web browser.

Or in your terminal run 
``` python3 main.py ```
and click on the http link that generates in your console for it to appear on your web browser.
