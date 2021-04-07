from application.models import db, Trip
from datetime import datetime
from flask_login import current_user


def insertTrip(formData):
    """Create a handler for our insert (POST) a trip.

    This function responds to a request to insert
    a new record into table 'trips' for a logged user
    """
    newTrip = Trip(
        admin_id=current_user.id,
        created=datetime.utcnow(),
        departure_date=formData.departure_date.data,
        departure_origin=formData.departure_origin.data,
        departure_destination=formData.departure_destination.data,
        return_date=formData.return_date.data,
        return_origin=formData.return_origin.data,
        return_destination=formData.return_destination.data,
        passenger_companion=formData.passenger_companion.data
    )
    db.session.add(newTrip)
    db.session.commit()
    return True


def readOneTrip(current_user_, trip_id_):
    """Create a handler to read (GET) one trip.

    This function uses trip_id to retrieve user's data
    for a single trip from table 'trips'
    """
    user_id = current_user_.id

    return Trip.query.filter_by(admin_id=user_id).filter(
        Trip.id==trip_id_
    ).first_or_404(description='There is no data with {}'.format(trip_id_))


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


def updateTrip(formData):
    """Create a handler for edit (POST) a trip.

    This function responds to a request to delete
    a record from table 'trips' for a logged user
    """
    trip = Trip.query.filter_by(id=formData.tripId.data).first()

    trip.departure_origin=formData.departure_origin.data
    trip.departure_destination=formData.departure_destination.data
    trip.departure_date=formData.departure_date.data
    trip.return_origin=formData.return_origin.data
    trip.return_destination=formData.return_destination.data
    trip.return_date=formData.return_date.data
    trip.passenger_companion=formData.passenger_companion.data
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
