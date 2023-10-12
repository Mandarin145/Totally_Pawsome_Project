import unittest
from flask import Flask
from utils import CustomerRepository, AnimalRepository, Customer, Customers, Animal, db
from _pytest.monkeypatch import MonkeyPatch


class TestCustomerRepositoryGetCustomer(unittest.TestCase):

    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    # no test to write
    def test_get_customers(self):
        pass


class TestCustomerRepositoryAddCustomer(unittest.TestCase):

    # initial setup of monkeypatch
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test_add_customer_when_cust_does_not_already_exist(self):
        # configuring the Flask connection to run the test, as the db in this function is a Flask feature
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'secret key'

        # creating an object of the Customer class for input to the function
        customer = Customer('12345678+bob.builder@gmail.com', 'bob', 'builder', '0123456789', 'bob.builder@gmail.com',
                            'bob street', 'bob city',
                            'bob state', 'bob zip')

        # running the test in the context of an app
        context = app.test_request_context()

        # creating two classes with attributes and methods for the monkeypatch
        # monkeypatch is pretending to run a query and pretending to connect to a DB
        # we are not testing the DB functionality here, just testing the function that executes these things

        # first class has methods to set the first customer as None to test the if clause of this function
        # to make sure customer is added to database when there is no pre-existing customer
        class FakeQuery:
            def filter_by(self, email):
                return self

            def first(self):
                return None

        # second class has methods mocking adding the customer info to the database and committing to the database
        class FakeDB:
            def session(self):
                return self

            def add(self, new_customer):
                return self

            def commit(self):
                return self

        # running the test within the context of the Flask app
        with context:
            # setting customer as None using FakeQuery class,
            # so we test that it will add customer to database in this situation using FakeDB class
            self.monkeypatch.setattr(Customers, 'query', FakeQuery())
            self.monkeypatch.setattr(db, 'session', FakeDB())

            # expected result from the test should be customer.id
            expected = customer.id

            # running the method of add_customer the CustomerRepository class
            result = CustomerRepository().customer_adopt(customer, 1234567)

            self.assertEqual(expected, result)

    def test_add_customer_when_cust_does_already_exist(self):
        # as above, Flask connection needs to be made and test run in the context of an app
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'secret key'
        context = app.test_request_context()

        # creating an object of the Customer class for input to the Monkeypatch function
        # pretending that this customer already exists in the database
        customer = Customer('12345678+bob.builder@gmail.com', 'bob', 'builder', '0123456789', 'bob.builder@gmail.com',
                            'bob street', 'bob city',
                            'bob state', 'bob zip')

        # FakeQuery class created again, this time with output that is the customer I just created
        class FakeQuery():
            def filter_by(self, email):
                return self

            def first(self):
                return customer

        # second class has methods mocking adding the adoption info to the database and committing to the database
        class FakeDB():
            def session(self):
                return self

            def add(self, new_customer):
                return self

            def commit(self):
                return self

        # again running in context of app
        with context:
            # setting customer as pre-defined customer
            self.monkeypatch.setattr(Customers, 'query', FakeQuery())
            self.monkeypatch.setattr(db, 'session', FakeDB())

            # creating second customer as input to the test function
            # expecting this ID to be changed to the ID of the customer that was originally already in database
            customer2 = Customer('987654321+bob.builder@gmail.com', 'bob', 'builder', '0123456789',
                                 'bob.builder@gmail.com', 'bob street', 'bob city', 'bob state', 'bob zip')

            # expected result from the test should be this pre-existing customer.id as they are already in database
            # customer2.id should be overwritten
            expected = customer.id

            # running the method of add_customer the CustomerRepository class
            result = CustomerRepository().customer_adopt(customer2, 1234567)

            self.assertEqual(expected, result)


class TestAnimalRepositoryGetToken(unittest.TestCase):

    # setup monkeypatch
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test_get_token_bad_response(self):
        # creating a class with an attribute set to have any status code that isn't 200
        # so the ValueError will be raised
        class BadResponse:
            status_code = 400

        # Monkeypatching to pretend the outcome of requests.post has a status code of 400
        self.monkeypatch.setattr('requests.post', lambda a, headers, data: BadResponse())

        # creating an instance of the AnimalRepository class so the get_token() method can be called
        animal = AnimalRepository()

        with self.assertRaises(ValueError):
            animal.get_token()

    def test_get_token_good_response(self):
        # creating a class with an attribute set to have status code 200
        # and a method to pretend to be running as the .json function
        # as the code will continue if status_code == 200, we are expecting a dictionary output
        class GoodResponse():
            status_code = 200
            def json(self):
                dict = {'access_token': 'token'}
                return dict

        # Monkeypatching to set the return value of the requests.post method to be GoodResponse()
        # so status code will be 200 and the json method can be applied
        self.monkeypatch.setattr('requests.post', lambda a, headers, data: GoodResponse())

        # creating an instance of the AnimalRepository() class so the get_token method can be called
        animal = AnimalRepository()

        # expecting the token within the dictionary output from json monkeypatch to be returned
        expected = 'token'
        self.assertEqual(expected, animal.get_token())


class TestAnimalRepositoryGetAnimalData(unittest.TestCase):

    # setup monkeypatch
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test_get_animal_data_bad_response(self):
        # creating an instance of the Animal() class to use as an input to the method
        animal_data = Animal('cat', 'small', True, True, True, True, True)

        # creating a class with an attribute set to have any status code that isn't 200
        # so the ValueError will be raised
        class BadResponse():
            status_code = 400

        # creating an instance of the AnimalRepository() class so the get_animal_data method can be called
        animal = AnimalRepository()

        # we already know the get_token() function works from test on get_token() written above
        # here I am just monkeypatching a response from this function to test the get_animal_data function
        self.monkeypatch.setattr(AnimalRepository, 'get_token', lambda _: 'test')

        # Monkeypatching to pretend the outcome of requests.post has a status code of 400
        self.monkeypatch.setattr('requests.get', lambda a, headers: BadResponse())

        with self.assertRaises(ValueError):
            animal.get_animal_data(animal_data)

    def test_get_animal_data_good_response(self):
        # creating an instance of the Animal() class to use as an input to the method
        animal_data = Animal('cat', 'small', True, True, True, True, True)

        # creating a class with an attribute set to have status code 200
        # and a method to pretend to be running as the .json function
        # as the code will continue if status_code == 200, we are expecting a dictionary output
        class GoodResponse():
            status_code = 200

            def json(self):
                dict = {'pagination': {'total_count': 4, 'count_per_page': 100},
                        'animals': ['animal1', 'animal2', 'animal3']}
                return dict

        #  creating an instance of the AnimalRepository() class so the get_animal_data method can be call
        animal = AnimalRepository()

        # we already know this works from test on get_token() written above
        # here I am just monkeypatching a response from this function to test the get_animal_data function
        self.monkeypatch.setattr(AnimalRepository, 'get_token', lambda _: 'test')

        # Monkeypatching to pretend the outcome of requests.post has a status code of 200
        self.monkeypatch.setattr('requests.get', lambda a, headers: GoodResponse())

        expected = ['animal1', 'animal2', 'animal3']

        self.assertEqual(expected, animal.get_animal_data(animal_data))


class TestAnimalRepositoryAgeCheck(unittest.TestCase):

    def test_age_check_senior_animal_in_list(self):
        # simple assertion test
        animals = [{"Name": "Fred", "age": "Senior"}, {"Name": "Teddy", "age": "Baby"}]
        # expecting only animals containing senior as value in dictionary to be added to the outcome dictionary
        expected = [{"Name": "Fred", "age": "Senior"}]
        animal = AnimalRepository()
        self.assertEqual(expected, animal.age_check(animals))

    def test_age_check_missing_senior_animal_in_list(self):
        # simple assertion test
        animals = [{"Name": "Fred", "age": "Baby"}, {"Name": "Teddy", "age": "Baby"}]
        # expecting only animals containing senior as value in dictionary to be added to the outcome dictionary
        expected = []
        animal = AnimalRepository()
        self.assertEqual(expected, animal.age_check(animals))


class TestAnimalRepositoryAnimalReturn(unittest.TestCase):

    def test_animal_return(self):
        # simple assertion test
        animal_list = [{"Name": "Fred", "age": "Senior"}, {"Name": "Teddy", "age": "Baby"}]
        # checking the generator function yields one dictionary at a time
        expected = {"Name": "Fred", "age": "Senior"}
        animal = AnimalRepository()
        self.assertEqual(expected, next(animal.animal_return(animal_list)))


class TestAnimalRepositoryAnimalInfo(unittest.TestCase):

    # setup monkeypatch
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test_animal_info_key_in_dict(self):
        # creating a class with a method to pretend to be running as the .json function
        class GoodResponse:
            def json(self):
                my_dict = {'animal': 'cat'}
                return my_dict

        self.monkeypatch.setattr(AnimalRepository, 'get_token', lambda _: 'test')

        self.monkeypatch.setattr('requests.get', lambda a, headers: GoodResponse())

        expected = 'cat'

        animal = AnimalRepository()
        self.assertEqual(expected, animal.animal_info('1234'))

    def test_animal_info_key_not_in_dict(self):
        # creating a class with a method to pretend to be running as the .json function
        class GoodResponse:
            def json(self):
                my_dict = {}
                return my_dict

        self.monkeypatch.setattr(AnimalRepository, 'get_token', lambda _: 'test')

        self.monkeypatch.setattr('requests.get', lambda a, headers: GoodResponse())

        animal = AnimalRepository()

        with self.assertRaises(KeyError):
            animal.animal_info('1234')


if __name__ == '__main__':
    unittest.main()
