"""CRUD forms for weights and trips"""
from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, FileField, SubmitField, validators
from wtforms.validators import InputRequired, DataRequired, Length, Optional

class AddWeightForm(FlaskForm):

  weight = FloatField('Weight',
                      validators=[InputRequired(),
                                  validators.NumberRange(min=20, max=200, message='Weight looks wrong!'),
                                  ])

  weightDate = DateField('Date',
                        validators=[InputRequired(),
                                    ])

  submit = SubmitField('Save')


class UploadFileForm(FlaskForm):

  txtFile = FileField('Only admitted txt and csv files',
                      [validators.Regexp(regex='^.*\\.(txt|csv)$', message='This file type is forbidden')])

  submit = SubmitField('Upload')

