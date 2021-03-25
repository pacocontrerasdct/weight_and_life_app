import os
from csv import DictReader
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import Seeder
from datetime import datetime
from application.models import Trip
from application.trip.crudAirport import readAirport

db = SQLAlchemy()

# All seeders inherit from Seeder
class LoadTripSeeds(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 15

    # run() will be called by Flask-Seeder
    def run(self):

        existingSeeds = Trip.query.filter_by(admin_id=6).first()

        if existingSeeds is None:

            fileName = 'trips.csv'
            filePath = os.path.join('application/static/uploads/', fileName) 
            
            with open(filePath, newline='') as csvfile:

                fNames = [
                    'origin_departure',
                    'destination_departure',
                    'date_departure',
                    'origin_return',
                    'destination_return',
                    'date_return',
                    'passenger_companion']
                reader = DictReader(csvfile, fieldnames=fNames, delimiter=';')
                tripList = []

                for row in reader:
                    
                    departure_origin_ = readAirport(airport_iata_identifier=row['origin_departure'])
                    departure_destination_ = readAirport(airport_iata_identifier=row['destination_departure'])
                    return_origin_ = readAirport(airport_iata_identifier=row['origin_return'])
                    return_destination_ = readAirport(airport_iata_identifier=row['destination_return'])

                    tripList.append(
                                    Trip(admin_id=6,
                                         departure_origin = departure_origin_.id,
                                         departure_destination = departure_destination_.id,
                                         departure_date = datetime.strptime((row['date_departure']), '%Y/%m/%d'),
                                         return_origin = return_origin_.id,
                                         return_destination = return_destination_.id,
                                         return_date = datetime.strptime((row['date_return']), '%Y/%m/%d'),
                                         passenger_companion = str(row['passenger_companion'])))

                if len(tripList) > 0:
                    self.db.session.bulk_save_objects(tripList)
