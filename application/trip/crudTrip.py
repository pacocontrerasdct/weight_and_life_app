from application.models import db, Admin, Trip
from datetime import datetime


def read(current_user_):
    """Create a handler for our read (GET) trips.

    This function responds to a request for table 'trips'
    with the complete list of trips
    """
    user_id = current_user_.id

    return Trip.query.filter_by(admin_id=user_id).order_by(
        Trip.ending_date.desc()).limit(5).all()


def insert(current_user_, starting_date_, ending_date_, from_airport_, to_airport_, solo_flight_):
    """Create a handler for our insert (POST) trips.

    This function responds to a request to insert
    a new record into table 'trips' for a logged user
    """
    newTrip = Trip(
        admin_id=current_user_.id,
        created=datetime.utcnow(),
        starting_date=starting_date_,
        ending_date=ending_date_,
        from_airport=from_airport_,
        to_airport=to_airport_,
        solo_flight=solo_flight_
    )
    db.session.add(newTrip)
    db.session.commit()
    return True


# def update(weightId_, weight_, date_):
#     """Create a handler for update (POST) a weight.

#     This function responds to a request to update
#     a record from table 'trips' for a logged user
#     """
#     weight = Trip.query.filter_by(id=weightId_).first()
#     weight.weight = weight_
#     weight.ending_date = date_
#     db.session.commit()
#     return True


# def edit(weightId_):
#     """Create a handler for edit (POST) a weight.

#     This function responds to a request to delete
#     a record from table 'trips' for a logged user
#     """
#     weight = Trip.query.filter_by(id=weightId_).first()
#     return weight


# def delete(weightId_):
#     """Create a handler for delete (POST) a weight.

#     This function responds to a request to delete
#     a record from table 'trips' for a logged user
#     """
#     weight = Trip.query.filter_by(id=weightId_).first()

#     db.session.delete(weight)
#     db.session.commit()
#     return True
