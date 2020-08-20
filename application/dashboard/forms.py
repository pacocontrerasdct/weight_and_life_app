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

dateWrongMsg = 'Date can\'t be in the future'
weightWrongMsg = (f"""That\'s not a valid weight!""",
                  f"""Weight is out of the scale 20 to 200kg.""")
fileForbMsg = 'This file type is forbidden. Use only txt or csv.'


class DataValidation(object):
    """
    This function initialises this class and
    set a default message
    """

    def __init__(self, message=None):
        super(DataValidation, self).__init__()
        if not message:
            message = 'Date is not valid.'
        self.message = message
    """
  This function checks if input date is a valid datetime instance
  and if it isn't in the future
  """
    def is_valid_date(form, field):
        d1 = field.data
        d2 = dt.now().date()

        if not isinstance(field.data, datetime.date):
            raise StopValidation()
        if d1 > d2:
            raise StopValidation(dateWrongMsg)
    """
  This function responds to a request for table 'weights'
  with the complete list of weights
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
                                       dataValidation.is_valid_date, ],
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
