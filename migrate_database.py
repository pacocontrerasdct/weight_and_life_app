"""
Flask-Migrate is an extension that handles 
SQLAlchemy database migrations for 
Flask applications using Alembic. 
The database operations are made available 
through the Flask command-line interface 
or through the Flask-Script extension.
Source: https://flask-migrate.readthedocs.io/en/latest/
---------------------------------------------------------

Using Miguel Grinberg step to add flask migrate to my project.
Source: https://blog.miguelgrinberg.com/post/how-to-add-flask-migrate-to-an-existing-project

# CREATE DATABASE weight_and_life_db; // create postgresql database using psql cli
# python3 migrate_database.py db init // initialise the repository for the migration
# python3 migrate_database.py db migrate // the migration creates a file inside 'versions' folder
# flask db stamp head // to tell Flaks-migrate and Alembic that the database is up to date
#
# flask db migrate + flask db upgrade // after changes to models, you will migrate, and then upgrade
"""

import os
from flask import Flask

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="postgresql:///weight_and_life_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Admin(UserMixin, db.Model):
    """Data model for Admin"""
    __tablename__ = 'administrators'

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(100),
                     index=False,
                     unique=False,
                     nullable=False)

    email = db.Column(db.String(120),
                      index=True,
                      unique=True,
                      nullable=False)

    password = db.Column(db.String(200),
                         index=True,
                         unique=False,
                         nullable=False)

    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=True,
                        default=datetime.utcnow())

    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)

    last_logout = db.Column(db.DateTime,
                            index=False,
                            unique=False,
                            nullable=True)

    full_access = db.Column(db.Boolean,
                            index=False,
                            unique=False,
                            nullable=True)

    weights = db.relationship(
        'Weight',
        backref='admin',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Weight.weight_date)'
    )

    trips = db.relationship(
        'Trip',
        backref='admin',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Trip.departure_date)'
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password"""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Admin {}>'.format(self.name)


class Subscriptor(db.Model):
    """Data model for Newsletter subscriptors"""
    __tablename__ = 'subscriptors'

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(64),
                     index=False,
                     unique=False,
                     nullable=False)

    email = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)

    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False,
                        default=datetime.utcnow())

    def __repr__(self):
        return '<Subscriptor {}>'.format(self.name)


class Weight(db.Model):
    """Data model for weights"""
    __tablename__ = 'weights'

    id = db.Column(db.Integer,
                   primary_key=True)

    admin_id = db.Column(db.Integer,
                         db.ForeignKey(Admin.id))

    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False,
                        default=datetime.utcnow())

    weight = db.Column(db.Float,
                       index=False,
                       unique=False,
                       nullable=False)

    weight_date = db.Column(db.DateTime,
                            index=False,
                            unique=False,
                            nullable=False)

    def __repr__(self):
        return '<Weight {}>'.format(self.weight)


class Trip(db.Model):
    """Data model for trips"""
    __tablename__ = 'trips'

    id = db.Column(db.Integer,
                   primary_key=True)

    admin_id = db.Column(db.Integer,
                         db.ForeignKey(Admin.id))

    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False,
                        default=datetime.utcnow())


    departure_origin = db.Column(db.Integer,
                                 index=False,
                                 unique=False,
                                 nullable=False)

    departure_destination = db.Column(db.Integer,
                                      index=False,
                                      unique=False,
                                      nullable=False)

    departure_date = db.Column(db.DateTime,
                               index=False,
                               unique=False,
                               nullable=False)

    return_origin = db.Column(db.Integer,
                              index=False,
                              unique=False,
                              nullable=False)

    return_destination = db.Column(db.Integer,
                                   index=False,
                                   unique=False,
                                   nullable=False)

    return_date = db.Column(db.DateTime,
                            index=False,
                            unique=False,
                            nullable=False)

    passenger_companion = db.Column(db.String(120),
                                    index=False,
                                    default="None",
                                    unique=False,
                                    nullable=False)

    def __repr__(self):
        return '<Trip {}>'.format(self.departure_date)


class Airport(db.Model):
    """Data model for Airports"""
    __tablename__ = 'airports'

    id = db.Column(db.Integer,
                   primary_key=True)

    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False,
                        default=datetime.utcnow())

    airport_country = db.Column(db.String(120),
                                index=False,
                                unique=False,
                                nullable=False)

    airport_city = db.Column(db.String(120),
                             index=True,
                             unique=False,
                             nullable=False)

    airport_name = db.Column(db.String(120),
                             index=False,
                             unique=False,
                             nullable=False)

    airport_iata_identifier = db.Column(db.String(3),
                                        index=True,
                                        unique=False,
                                        nullable=False)

    def __repr__(self):
        return '<Trip {}>'.format(self.airport_country)


if __name__ == '__main__':
    manager.run()
