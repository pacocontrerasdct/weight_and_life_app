import os
from csv import DictReader
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import Seeder
from datetime import datetime
from application.models import Weight

db = SQLAlchemy()

# All seeders inherit from Seeder
class LoadWeightSeeds(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 10

    # run() will be called by Flask-Seeder
    def run(self):

        existingSeeds = Weight.query.filter_by(admin_id=6).first()

        if existingSeeds is None:

            fileName = 'weights.csv'
            filePath = os.path.join('application/static/uploads/', fileName) 
            
            with open(filePath, newline='') as csvfile:

                fNames = ['weight', 'date']
                reader = DictReader(csvfile, fieldnames=fNames, delimiter=';')
                weightList = []

                for row in reader:
                    weightList.append(
                                      Weight(admin_id=6,
                                             weight=float(row['weight']),
                                             weight_date=datetime.strptime((row['date']),
                                                                           '%Y/%m/%d')))

                if len(weightList) > 0:
                    self.db.session.bulk_save_objects(weightList)
