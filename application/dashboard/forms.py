"""CRUD forms for weights and trips"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import FloatField, DateField, HiddenField, SubmitField, validators
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
                      validators=[FileRequired(),
                                  FileAllowed(['txt','csv'], 'This file type is forbidden. Use only txt or csv.')])
  submit = SubmitField('Upload')


class DeleteWeightForm(FlaskForm):
  weightId = HiddenField('weightId')
  submit = SubmitField('X')


class EditWeightForm(FlaskForm):
  weightId = HiddenField('weightId')
  submit = SubmitField('E')

