import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Stations = Base.classes.stations
#Measurements = Base.classes.measurements

# Create our session (link) from Python to the DB
session = Session(engine)
conn = engine.connect()


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#####
'''/api/v1.0/precipitation

Query for the dates and temperature observations from the last year.
Convert the query results to a Dictionary using date as the key and tobs as the value.
Return the json representation of your dictionary.

/api/v1.0/stations

Return a json list of stations from the dataset.

/api/v1.0/tobs

Return a json list of Temperature Observations (tobs) for the previous year

/api/v1.0/<start> and /api/v1.0/<start>/<end>

Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.'''
#####

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return  dates and temperature observations from the last year."""

    precip_df = pd.read_sql("SELECT date, prcp FROM measurements", conn)
    precip_df = precip_df.set_index("date")
    all_obvs = []
    for row in precip_df:
        date_temp_dict = {}
        date_temp_dict["date"] = row.date
        date_temp_dict["temp"] = row.prcp
        all_obvs.append(date_temp_dict)

    return jsonify(all_obvs)
'''
@app.route("/api/v1.0/passengers")
def passengers():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for passenger in results:
        passenger_dict = {}
        passenger_dict["name"] = passenger.name
        passenger_dict["age"] = passenger.age
        passenger_dict["sex"] = passenger.sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)'''


if __name__ == '__main__':
    app.run(debug=True)
