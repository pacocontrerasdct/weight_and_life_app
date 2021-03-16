"""CRUD forms for trips"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField,
                     DateField,
                     HiddenField,
                     SelectField,
                     SubmitField,
                     validators)
from wtforms.validators import (InputRequired,
                                DataRequired,
                                Length,
                                Optional,
                                ValidationError,
                                StopValidation)
import datetime
from datetime import datetime as dt
from markupsafe import Markup

from application.trip.crudAirport import readAirport, readAirportList

airportsList = readAirportList()

dateInvalidMsg = f'''Data is not valid'''
dateWrongMsg = f'''Date is in a wrong format'''
selectOneMsg = f'''You need to select airports for departure and return'''
invalidCharMsg = f'''Companion name contains this forbidden character'''


class DataValidation(object):
    """
    Initialises and set a default message
    """
    def __init__(self, message=None):
        super(DataValidation, self).__init__()
        if not message:
            self.message = dateInvalidMsg
    """
    Check if errors list is empty
    """
    def isFormErrorsEmpty(form, error):
        if error not in form.errors:
            form.errors.add(error)
    """
    Check if user input is valid
    """
    def validate_input(form, field):
        excluded_chars = "*?!'^+-%&/()=}]|[{£$#\\"
        for char in field.data:
            if char in excluded_chars:
                DataValidation.isFormErrorsEmpty(form, 
                                  f'''{invalidCharMsg} \'{char}\'''')
                raise ValidationError()
    """
    Checks if input date is a valid datetime instance
    and if it is in the future
    """
    def is_valid_date(form, field):
        if not isinstance(field.data, datetime.date):
            DataValidation.isFormErrorsEmpty(form, dateWrongMsg)
            raise StopValidation(dateInvalidMsg or field.gettext(
                'Date is novild!'
            )) 
    """
    Checks there is a selected airport
    different from the default 'select one' option
    """
    def is_valid_airport_id(form, field):
        if int(field.data) == int(form.default):
            DataValidation.isFormErrorsEmpty(form, selectOneMsg)
            raise ValidationError(selectOneMsg)

dataValidation = DataValidation

class AddTripForm(FlaskForm):

    errors = set()

    default = readAirport(airport_city='Select one').id


    tripId = HiddenField('tripId',
                           default={},)

    departure_origin = SelectField('From:',
                                   coerce=int,
                                   validators=[
                                        InputRequired(),
                                        dataValidation.is_valid_airport_id
                                   ],
                                   choices = airportsList,
                                   default=default)

    departure_destination = SelectField('To:',
                                        coerce=int,
                                        validators=[
                                            InputRequired(),
                                            dataValidation.is_valid_airport_id
                                        ],
                                        choices = airportsList,
                                        default=default)

    departure_date = DateField('Date',
                               format='%Y-%m-%d',
                               validators=[InputRequired(),
                                    dataValidation.is_valid_date],
                               default={})

    return_origin = SelectField('From:',
                                coerce=int,
                                validators=[
                                    InputRequired(),
                                    dataValidation.is_valid_airport_id
                                ],
                                choices = airportsList,
                                default=default)

    return_destination = SelectField('To:',
                                     coerce=int,
                                     validators=[
                                        InputRequired(),
                                        dataValidation.is_valid_airport_id
                                    ],
                                    choices = airportsList,
                                    default=default)

    return_date = DateField('Date',
                            format='%Y-%m-%d',
                            validators=[InputRequired(),
                            dataValidation.is_valid_date],
                            default={})  

    passenger_companion = StringField('Companions',
                                      validators=[
                                        Length(max=50),
                                        dataValidation.validate_input
                                    ],
                                    default="")

    submit = SubmitField('Add')


class EditTripForm(FlaskForm):
    tripId = HiddenField('tripId')
    submit = SubmitField('Edit')


class UpdateTripForm(FlaskForm):
    tripId = HiddenField('tripId')
    tripFormData = HiddenField('tripFormData')
    submit = SubmitField('Update')


class DeleteTripForm(FlaskForm):
    tripId = HiddenField('tripId')
    formName = HiddenField('formName')
    submit = SubmitField('Delete')
