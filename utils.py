import logging
import os
from itertools import compress
from math import ceil

import requests
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
                    format='%(name)s - %(levelname)s - %(message)s')

"""initialising database"""

db = SQLAlchemy()


class Customers(db.Model):
    # nothing to set therefore no __init__
    # id of the animal associated with the customer
    id = db.Column(db.String(255), primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city_name = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))


class CustomerAdoptions(db.Model):
    pet_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(255), db.ForeignKey("customers.id"))


"""class to hold customer information"""


class Customer:
    def __init__(self, customer_id, firstname, lastname, phone, email, address, city_name, state, zipcode):
        self.id = customer_id
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email
        self.address = address
        self.city_name = city_name
        self.state = state
        self.zipcode = zipcode


class CustomerAdoption:
    def __init__(self, pet_id, customer_id):
        self.pet_id = pet_id
        self.customerID = customer_id


class Animal:
    def __init__(self, cat_or_dog, select_size, select_good_with_children, select_good_with_dogs,
                 select_good_with_cats, select_house_trained, select_special_needs):
        self.cat_or_dog = cat_or_dog
        self.select_size = select_size
        self.select_good_with_children = select_good_with_children
        self.select_good_with_dogs = select_good_with_dogs
        self.select_good_with_cats = select_good_with_cats
        self.select_house_trained = select_house_trained
        self.select_special_needs = select_special_needs


"""class for working with customer information"""


class CustomerRepository:
    # nothing to set therefore no __init__

    """getting customer info from database"""

    @staticmethod
    def get_customers():
        error = ''
        customer = Customers.query.filter_by().all()
        return [customer, error]

    """Adding customer to database"""

    @staticmethod
    def customer_adopt(customer_data, pet_id):
        new_adoption = CustomerAdoptions(pet_id=pet_id, customer_id=customer_data.id)

        customer = Customers.query.filter_by(email=customer_data.email).first()
        if customer is None:
            firstname = customer_data.firstname
            lastname = customer_data.lastname
            phone = customer_data.phone
            email = customer_data.email
            address = customer_data.address
            city_name = customer_data.city_name
            state = customer_data.state
            zipcode = customer_data.zipcode

            new_customer = Customers(id=customer_data.id, firstname=firstname, lastname=lastname, phone=phone,
                                     email=email, address=address, city_name=city_name, state=state, zipcode=zipcode)
            db.session.add(new_customer)
        else:
            new_adoption.customer_id = customer.id

        db.session.add(new_adoption)
        db.session.commit()
        return new_adoption.customer_id


"""class for working with animal information"""


class AnimalRepository:
    # nothing to set therefore no __init__

    """Requesting access token"""

    @staticmethod
    def get_token():

        url = "https://api.petfinder.com/v2/oauth2/token"

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = f"grant_type=client_credentials&client_id={API_KEY}&client_secret={API_SECRET}"

        resp = requests.post(url, headers=headers, data=data)

        # tracking response code - if not 200 there is a problem
        logging.info(f'Response code {resp}')
        if resp.status_code != 200:
            raise ValueError(f'Bad connection, response not 200, it is {resp.status_code}')
        response = resp.json()
        logging.info(f'resp.json returns dictionary {response} inc. access token')
        token = response['access_token']
        logging.info(f'access token successfully generated')
        return token

    """Connecting to API and retrieving data based on user choice from form"""

    def get_animal_data(self, animal_data):

        logging.info(f"User specified choices were {animal_data.cat_or_dog}, "
                     f"size = {animal_data.select_size}, "
                     f"good with children = {animal_data.select_good_with_children}, "
                     f"good with dogs = {animal_data.select_good_with_dogs}, "
                     f"good with cats = {animal_data.select_good_with_cats}, "
                     f"house trained = {animal_data.select_house_trained}, "
                     f"special needs = {animal_data.select_special_needs}")

        all_pets = []

        url = f"https://api.petfinder.com/v2/animals?type={animal_data.cat_or_dog}&size={animal_data.select_size}" \
              f"&good_with_children={str(animal_data.select_good_with_children).lower()}" \
              f"&good_with_dogs{str(animal_data.select_good_with_dogs).lower()}" \
              f"&good_with_cats={str(animal_data.select_good_with_cats).lower()}" \
              f"&house_trained={str(animal_data.select_house_trained).lower()}" \
              f"&special_needs={str(animal_data.select_special_needs).lower()}&status=adoptable&limit=100"

        auth_token = self.get_token()
        response = requests.get(url, headers={"Authorization": f"Bearer {auth_token}"})

        logging.info(f'Response code {response}')
        if response.status_code != 200:
            raise ValueError(f'Bad connection, response not 200, response code is {response.status_code}')
        json_response = response.json()
        # total amount of pets divided by maximum amount of pets on each page to give the amount of pages to go through.
        # to make sure gets all data from api
        page_count = ceil(json_response['pagination']['total_count'] / json_response['pagination']['count_per_page'])
        # each page gives list of dictionaries
        all_pets.extend(json_response['animals'])

        # to go through each of the pages.
        next_page = 1
        while next_page < page_count:
            # do the same thing
            response = requests.get(f"{url}&page={next_page + 1}", headers={"Authorization": f"Bearer {auth_token}"})
            json_page = response.json()
            all_pets.extend(json_page['animals'])
            # increment page each time we go through
            next_page += 1
        return all_pets

    """Returning only those animals which are older"""

    def age_check(self, animals):
        # placeholder data, to be replaced with output from the search
        # animals = [{"Name": "Fred", "age": "senior"}, {"Name": "Teddy", "age": "baby"}]
        selector = [True if animal['age'] == 'Senior' else False for animal in animals]
        senior_animals = compress(animals, selector)
        output = list(senior_animals)
        if not output:
            logging.info("No senior pets in user selection")
        return output

    """Generator function to display one animal at a time - to be reviewed"""

    def animal_return(self, animal_list):
        for animal in animal_list:
            yield animal

    """Function to get individual animal info"""
    def animal_info(self, pet_id):
        auth_token = self.get_token()
        response = requests.get(f'https://api.petfinder.com/v2/animals/{pet_id}',
                                headers={"Authorization": f"Bearer {auth_token}"})
        animal_response = response.json()
        return animal_response['animal']


