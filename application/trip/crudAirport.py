from application.models import Airport

def readAirportList():
    """Create a handler for our read (GET) Airports data.

    This function responds to a request for table 'Airports'
    with the complete list of Airports data
    """
    airportsList_ = []
    try:

        airportsList_ = [
            (airportsList.id,
                f'''{airportsList.airport_city}, {airportsList.airport_name}''' 
                if 
                    airportsList.airport_name
                else
                    f'''{airportsList.airport_city}'''

            ) for airportsList in Airport.query
                .order_by('airport_city')
                .filter(Airport.airport_city != '')
        ]

    except Exception as e:
        print("No Airport list loaded yet!")

    return airportsList_


def readAirport(**kwargs):
    """Create a handler for reading a single airport data.

    This function respond to a request for table 'Airports'
    with a single airport data: Country, City, Airport Name, IATA identifier
    """
    airport_ = []
    try:
        airport_ = Airport.query.filter_by(**kwargs).first()
    except Exception as e:
        print("No Airport found!")

    return airport_
