"""CRUD forms for weights and trips"""
from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, FileField, HiddenField, SubmitField, validators
from wtforms.validators import InputRequired, DataRequired, Length, Optional, ValidationError
from datetime import datetime as dt

class AddWeightForm(FlaskForm):

  def is_not_in_future(self, weightDate):
    if type(weightDate.data) == 'datetime.date' and weightDate.data > dt.now().date():
      raise ValidationError('Date can\'t be in the future')

  weightId = HiddenField('weightId',
                          default={},)
  weight = FloatField('Weight',
                      validators=[InputRequired(),
                                  validators.NumberRange(min=20, max=200, message='Weight looks wrong!')],
                      default={},)
  weightDate = DateField('Date',
                        format='%Y-%m-%d',
                        validators=[InputRequired(),
                                    is_not_in_future],
                        default={},)
  submit = SubmitField('Save')


class UploadFileForm(FlaskForm):
  txtFile = FileField('Only admitted txt and csv files',
                      [validators.Regexp(regex='^.*\\.(txt|csv)$', message='This file type is forbidden')])
  submit = SubmitField('Upload')


class DeleteWeightForm(FlaskForm):
  weightId = HiddenField('weightId')
  submit = SubmitField('X')


class EditWeightForm(FlaskForm):
  weightId = HiddenField('weightId')
  submit = SubmitField('E')

