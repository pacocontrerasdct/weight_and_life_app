"""CRUD forms for weights and trips"""
import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import DecimalField, DateField, HiddenField, SubmitField, validators
from wtforms.validators import InputRequired, DataRequired, Length, Optional, ValidationError, StopValidation
from datetime import datetime as dt

class DataValidation(object):
  """Validates date type
  and if date is in the future"""

  def __init__(self, message=None):
    super(DataValidation, self).__init__()
    if not message:
      message = 'Date is not valid.'
    self.message = message

  def is_a_valid_date(form, field):
    if not isinstance(field.data, datetime.date):
      raise StopValidation()

  def is_not_a_future_date(form, field):
    if field.data > dt.now().date():
      raise StopValidation('Date can\'t be in the future')
    
dataValidation = DataValidation

class AddWeightForm(FlaskForm):

  weightId = HiddenField('weightId',
                          default={},)
  weight = DecimalField('Weight',
                        places=3,
                        validators=[InputRequired(),
                                    validators.NumberRange(min=20, max=200, message='Weight looks wrong!')],
                        default={},)
  weightDate = DateField('Date',
                        format='%Y-%m-%d',
                        validators=[InputRequired(),
                                    dataValidation.is_a_valid_date,
                                    dataValidation.is_not_a_future_date,],
                        default={},)
  submit = SubmitField('Save')


class UploadFileForm(FlaskForm):
  file = FileField('Only admitted txt and csv files',
                      validators=[FileRequired(),
                                  FileAllowed(['txt','csv'], 'This file type is forbidden. Use only txt or csv.')])
  submit = SubmitField('Upload')


class DeleteWeightForm(FlaskForm):
  weightId = HiddenField('weightId')
  submit = SubmitField('X')


class EditWeightForm(FlaskForm):
  weightId = HiddenField('weightId')
  submit = SubmitField('E')

