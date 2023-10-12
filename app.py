import os
import time

import requests
from flask import Flask, request, render_template, flash

from forms import CustomerForm, PetSearchForm
from utils import CustomerRepository, AnimalRepository, db, Customer, Animal
from dotenv import load_dotenv

load_dotenv()

database_password = os.getenv('DATABASE_PASSWORD')
database_user = os.getenv('DATABASE_USER')
app = Flask(__name__)
# Add database using flask_sqlalchemy import SQLAlchemy:
# app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://username:password@local'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{database_user}:{database_password}@localhost/adoption'
app.config['SECRET_KEY'] = 'secret key'

customer_repository = CustomerRepository()
animal_repository = AnimalRepository()


# add routes here
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template('about_us.html')


@app.route('/customer', methods=['GET', 'POST'])
def customer_form():
    form = CustomerForm()

    if request.method == 'POST':
        pet_id = request.args.get('pet_id')
        customer_id = str(time.time()) + form.email.data
        customer = Customer(customer_id, form.firstname.data, form.lastname.data, form.phone.data,
                            form.email.data, form.address.data, form.city_name.data, form.state.data, form.zipcode.data)

        customer_repository.customer_adopt(customer, pet_id)

        flash(f'Customer {form.firstname.data} successfully adopted a new pet!', 'success')
        form.clear()

        animal = animal_repository.animal_info(pet_id)

        return render_template('thanks.html', adopted_animal=animal)

    return render_template('customer.html', form=form)


@app.route('/admin', methods=['GET'])
def show_customers():
    result = customer_repository.get_customers()
    customer = result[0]
    error = result[1]

    return render_template('customer_list.html', customer=customer, message=error)


@app.route('/adopt', methods=['GET', 'POST'])
def pet_search_form():
    form = PetSearchForm()

    if request.method == 'POST':
        user_selection = Animal(form.cat_or_dog.data, form.select_size.data, form.select_good_with_children.data,
                                form.select_good_with_dogs.data,
                                form.select_good_with_cats.data, form.select_house_trained.data,
                                form.select_special_needs.data)

        all_pets = animal_repository.get_animal_data(user_selection)
        senior_animals = animal_repository.age_check(all_pets)
        if senior_animals == []:
            print("all")
            return render_template('pet_list.html', form_selection=form, pets=all_pets)
        else:
            print("senior")
            return render_template('pet_list.html', form_selection=form, pets=senior_animals)

    return render_template('adopt_form.html', form=form)


def run():
    db.init_app(app)
    app.run(debug=True, port=5002)



