"""CRUD forms for weights and trips"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (DecimalField,
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
weightWrongMsg = (f"""That's not a valid weight! """
                  f"""Weight is out of the scale from 20 to 200 kg.""")
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
    """
    Check if weight is between a valid range of weights
    """
    def is_valid_weight(form, field):
        try:
            weight = float(field.data)
            if weight < 20 or weight > 200:
                raise StopValidation(weightWrongMsg)
        except Exception as e:
            raise StopValidation(weightWrongMsg)


dataValidation = DataValidation


class AddWeightForm(FlaskForm):

    weightId = HiddenField('weightId',
                           default={},)
    weight = DecimalField('Weight',
                          places=3,
                          validators=[InputRequired(),
                                      dataValidation.is_valid_weight],
                          default={},)
    weightDate = DateField('Date',
                           format='%Y-%m-%d',
                           validators=[InputRequired(),
                                       dataValidation.is_valid_date],
                           default={},)
    submit = SubmitField('Save')


class UploadFileForm(FlaskForm):
    file = FileField('Only admitted txt and csv files',
                     validators=[FileRequired(),
                                 FileAllowed(['txt', 'csv'], fileForbMsg)])
    submit = SubmitField('Upload')


class DeleteWeightForm(FlaskForm):
    weightId = HiddenField('weightId')
    submit = SubmitField('X')


class EditWeightForm(FlaskForm):
    weightId = HiddenField('weightId')
    submit = SubmitField('E')
