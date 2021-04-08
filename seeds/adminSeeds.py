from flask_sqlalchemy import SQLAlchemy
from flask_seeder import Seeder
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import Admin

db = SQLAlchemy()

# All seeders inherit from Seeder
class LoadAdminSeeds(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    # run() will be called by Flask-Seeder
    def run(self):
        
        existingSeeds = Admin.query.filter_by(email='pacocontrerasdct@gmail.com').first()

        if existingSeeds is None:

            adminList = []

            # author admin
            admin = Admin(name='Paco',
                          email='pacocontrerasdct@gmail.com',
                          full_access=True)
            admin.set_password('123456')
            adminList.append(admin)

            # sample admin
            admin = Admin(name='John Doe',
                          email='joe.doe@gmail.com',
                          full_access=False)
            admin.set_password('123456')
            adminList.append(admin)

            if len(adminList) > 0:
                self.db.session.bulk_save_objects(adminList)
