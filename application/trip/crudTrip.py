from application.models import db, Admin, Trip
from datetime import datetime


def read(current_user_):
    """Create a handler for our read (GET) trips.

    This function responds to a request for table 'trips'
    with the complete list of trips
    """
    user_id = current_user_.id

    return Trip.query.filter_by(admin_id=user_id).order_by(
        Trip.return_date.desc()).limit(5).all()


def insert(current_user_,
           departure_origin_,
           departure_destination_,
           departure_date_,
           return_origin_,
           return_destination_,
           return_date_,
           passenger_companion_):
    """Create a handler for our insert (POST) trips.

    This function responds to a request to insert
    a new record into table 'trips' for a logged user
    """
    newTrip = Trip(
        admin_id=current_user_.id,
        created=datetime.utcnow(),
        departure_date=departure_date_,
        departure_origin=departure_origin_,
        departure_destination=departure_destination_,
        return_date=return_date_,
        return_origin=return_origin_,
        return_destination=return_destination_,
        passenger_companion=passenger_companion_
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
#     weight.return_date = date_
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
