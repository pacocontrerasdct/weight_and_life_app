from application.models import db, Trip
from datetime import datetime
from sqlalchemy.sql.expression import or_


def readAllTrips(current_user_, flag_trip_type = 'default'):
    """Create a handler to read (GET) all trips.

    This function responds to a request for table 'trips'
    with the complete list of trips, or a partial list
    if a flag_trip_type is found
    """
    user_id = current_user_.id

    if flag_trip_type == 'solo':
        tripType = Trip.passenger_companion == ''
    elif flag_trip_type == 'group':
        tripType = Trip.passenger_companion != ''
    else:
        tripType = Trip.passenger_companion.like('%')

    return Trip.query.filter_by(admin_id=user_id).filter(
        tripType
    ).order_by(Trip.return_date.desc()).all()


def readOneTrip(current_user_, trip_id_):
    """Create a handler to read (GET) one trip.

    This function uses trip_id to retrieve user's data
    for a single trip from table 'trips'
    """
    user_id = current_user_.id

    return Trip.query.filter_by(admin_id=user_id).filter(
        Trip.id==trip_id_
    ).first_or_404(description='There is no data with {}'.format(trip_id_))


def insertTrip(current_user_,
           departure_origin_,
           departure_destination_,
           departure_date_,
           return_origin_,
           return_destination_,
           return_date_,
           passenger_companion_):
    """Create a handler for our insert (POST) a trip.

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

def insertTrip2(**kargs):
    """Create a handler for our insert (POST) a trip.

    This function responds to a request to insert
    a new record into table 'trips' for a logged user
    """

    print(**kargs)

    # newTrip = Trip(
    #     admin_id=current_user_.id,
    #     created=datetime.utcnow(),
    #     departure_date=departure_date_,
    #     departure_origin=departure_origin_,
    #     departure_destination=departure_destination_,
    #     return_date=return_date_,
    #     return_origin=return_origin_,
    #     return_destination=return_destination_,
    #     passenger_companion=passenger_companion_
    # )
    # db.session.add(newTrip)
    # db.session.commit()
    # return True

def updateTrip(tripId_,
         departure_origin_,
         departure_destination_,
         departure_date_,
         return_origin_,
         return_destination_,
         return_date_,
         passenger_companion_):
    """Create a handler for edit (POST) a trip.

    This function responds to a request to delete
    a record from table 'trips' for a logged user
    """
    trip = Trip.query.filter_by(id=tripId_).first()
    trip.departure_origin=departure_origin_
    trip.departure_destination=departure_destination_
    trip.departure_date=departure_date_
    trip.return_origin=return_origin_
    trip.return_destination=return_destination_
    trip.return_date=return_date_
    trip.passenger_companion=passenger_companion_
    db.session.commit()
    return True


def deleteTrip(tripId_):
    """Create a handler for delete (POST) a trip.

    This function responds to a request to delete
    a record from table 'trips' for a logged user
    """
    trip = Trip.query.filter_by(id=tripId_).first()
    db.session.delete(trip)
    db.session.commit()
    return True
