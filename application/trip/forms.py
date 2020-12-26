"""CRUD forms for weights and trips"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField,
                     DateField,
                     HiddenField,
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

dateInvalidMsg = f"""Date is not valid."""
dateWrongMsg = f"""Date can't be in the future"""
fileForbMsg = f"""This file type is forbidden. Use only txt or csv."""


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
        d1 = field.data
        d2 = dt.now().date()

        if not isinstance(field.data, datetime.date):
            raise StopValidation()
        if d1 > d2:
            raise StopValidation(dateWrongMsg)


dataValidation = DataValidation


class AddTripForm(FlaskForm):

    tripId = HiddenField('tripId',
                           default={},)

    departure_origin = StringField('From Airport',
                        validators=[InputRequired()],
                        default={},)

    departure_destination = StringField('To Airport',
                        validators=[InputRequired()],
                        default={},)

    departure_date = DateField('Date',
                           format='%Y-%m-%d',
                           validators=[InputRequired(),
                                       dataValidation.is_valid_date],
                           default={},)

    return_origin = StringField('From Airport',
                        validators=[InputRequired()],
                        default={},)

    return_destination = StringField('To Airport',
                        validators=[InputRequired()],
                        default={},)

    return_date = DateField('Date',
                           format='%Y-%m-%d',
                           validators=[InputRequired(),
                                       dataValidation.is_valid_date],
                           default={},)  

    passenger_companion = StringField('Companions',
                        validators=[],
                        default={"None"},)

    submit = SubmitField('Add trip')
