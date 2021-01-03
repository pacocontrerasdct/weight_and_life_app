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

from application.trip.crudAirport import readAirport

defaultSelectorRow = readAirport(airport_city='Select one')

dateInvalidMsg = f"""Data is not valid."""
dateWrongMsg = f"""Date is in a wrong format."""
selectOneMsg = f"""You need to select Airports for departure and return."""


class DataValidation(object):
    """
    Initialises and set a default message
    """
    def __init__(self, message=None):
        super(DataValidation, self).__init__()
        if not message:
            self.message = dateInvalidMsg
    """
    Checks if input date is a valid datetime instance
    and if it is in the future
    """
    def is_valid_date(form, field):
        if not isinstance(field.data, datetime.date):
            form.errors.append(dateWrongMsg)
            raise StopValidation()
    """
    Checks there is a selected airport
    different from the default 'select one' option
    """
    def is_valid_airport_id(form, field):
        if field.data == 1:
            form.errors.append(selectOneMsg)
            raise StopValidation()

dataValidation = DataValidation


class AddTripForm(FlaskForm):

    errors = []

    tripId = HiddenField('tripId',
                           default={},)

    departure_origin = SelectField('From:',
                                   coerce=int,
                                   validators=[
                                        InputRequired(),
                                        dataValidation.is_valid_airport_id
                                   ],
                                   default=defaultSelectorRow.id)

    departure_destination = SelectField('To:',
                                        coerce=int,
                                        validators=[
                                            InputRequired(),
                                            dataValidation.is_valid_airport_id
                                        ],
                                        default=defaultSelectorRow.id)

    departure_date = DateField('Date',
                               format='%Y-%m-%d',
                               validators=[InputRequired(),
                                    dataValidation.is_valid_date],
                               default={},)

    return_origin = SelectField('From:',
                                coerce=int,
                                validators=[
                                    InputRequired(),
                                    dataValidation.is_valid_airport_id
                                ],
                                default=defaultSelectorRow.id)

    return_destination = SelectField('To:',
                                     coerce=int,
                                     validators=[
                                        InputRequired(),
                                        dataValidation.is_valid_airport_id
                                    ],
                                    default=defaultSelectorRow.id)

    return_date = DateField('Date',
                            format='%Y-%m-%d',
                            validators=[InputRequired(),
                                dataValidation.is_valid_date],
                            default={},)  

    passenger_companion = StringField('Companions',
                                      validators=[],
                                      default={},)

    submit = SubmitField('Add trip')
