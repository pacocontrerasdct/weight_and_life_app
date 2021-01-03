"""General forms"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (SubmitField,
                     validators)

fileForbMsg = f"""This file type is forbidden. Use only txt or csv."""


class UploadFileForm(FlaskForm):
    file = FileField('Only admitted txt and csv files',
                     validators=[FileRequired(),
                                 FileAllowed(['txt', 'csv'], fileForbMsg)])
    submit = SubmitField('Upload')