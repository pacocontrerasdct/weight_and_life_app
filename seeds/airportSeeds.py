import os
from csv import DictReader
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import Seeder
from datetime import datetime
from application.models import Airport

db = SQLAlchemy()

# All seeders inherit from Seeder
class LoadAirportSeeds(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 5

    # run() will be called by Flask-Seeder
    def run(self):

        existingSeeds = Airport.query.filter_by(airport_city='Bamyan').first()

        if existingSeeds is None:
            
            fileName = 'airport_list_dataset.csv'
            filePath = os.path.join('application/static/uploads/', fileName)

            with open(filePath, newline='') as csvfile:
                fNames = ['airport_country', 'airport_city', 'airport_name', 'iata_identifier']
                reader = DictReader(csvfile, fieldnames=fNames, delimiter=';')
                airportList = []
                
                for row in reader:
                    airportList.append(
                                      Airport(
                                              airport_country=row['airport_country'],
                                              airport_city=row['airport_city'],
                                              airport_name=row['airport_name'],
                                              airport_iata_identifier=row['iata_identifier']))

                if len(airportList) > 0:
                    self.db.session.bulk_save_objects(airportList)
