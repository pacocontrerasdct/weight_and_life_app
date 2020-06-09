"""CRUD forms for weights and trips"""
from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, FileField, SubmitField, validators
from wtforms.validators import InputRequired, DataRequired, Length, Optional

class AddWeightForm(FlaskForm):

  weight = FloatField('Weight',
                      validators=[InputRequired(),
                                  Length(min=2, message='You can\'t weight that little. Please correct the number'),
                                  Length(max=6, message='That weight is too high. Please correct the number'),
                                  ])

  weightDate = DateField('Date',
                        validators=[InputRequired(),
                                    Length(min=10, message='You can\'t weight that little. Please correct the number'),
                                    Length(max=10, message='That weight is too high. Please correct the number'),
                                    ])

  submit = SubmitField('Save')


class UploadFileForm(FlaskForm):
  match='link_high_sierra.txt'

  txtFile = FileField('Upload a file [only txt or csv]',
                  [validators.regexp(match, message='This file type is forbidden')])

  submit = SubmitField('Upload')

