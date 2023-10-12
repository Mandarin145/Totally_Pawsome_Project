from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired, InputRequired


class CustomerForm(FlaskForm):
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    phone = StringField("Phone number")
    email = StringField("Email address", validators=[DataRequired()])
    address = StringField("Address")
    city_name = StringField("City")
    state = StringField("State")
    zipcode = StringField("Zipcode")
    submit = SubmitField("Submit")

    def clear(self):
        self.firstname.data = ''
        self.lastname.data = ''
        self.phone.data = ''
        self.email.data = ''
        self.address.data = ''
        self.city_name.data = ''
        self.state.data = ''
        self.zipcode.data = ''


class PetSearchForm(FlaskForm):
    cat_or_dog = RadioField('Are you looking for a cat or a dog?', choices=['Cat', 'Dog'], validators=[InputRequired()])
    select_size = RadioField('Size of pet', choices=['Small', 'Medium', 'Large'], validators=[InputRequired()])
    select_good_with_children = BooleanField('Good with children', default=False)
    select_good_with_cats = BooleanField('Good with other cats', default=False)
    select_good_with_dogs = BooleanField('Good with dogs', default=False)
    select_house_trained = BooleanField('House trained', default=False)
    select_special_needs = BooleanField('Special needs', default=False)
    send = SubmitField('Send')
