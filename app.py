#Dependencies

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask Set up

app = Flask(__name__)

#Home page and list of all routes
@app.route("/")
def welcome():
    return(
        f"Welcome to Hawaii Climate App<br/>"
        f"Routes Available:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperature Observations: /api/v1.0/tobs<br/>"
        f"1 year Temp: /api/v1.0/temp/2016/2017"
    )


#precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= dt.date(2016,8,23)).\
        filter(Measurement.date <= dt.date(2017,8,23)).all()
    
    # Dict of dates and prcp values
    prcps = []
    for date, prcp in precipitation:
        precipitations_dict  = {}
        precipitations_dict ["date"] = date
        precipitations_dict ["prcp"] = prcp
        prcps.append(precipitations_dict)
    #jsonify
    return jsonify(prcps)


#stations
@app.route("/api/v1.0/stations")
def stations():
    #Query of stations data
    stations_data = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

   # Dict of data to jsonify
    stations = []

    for id, station, name, latitude, longitude, elevation in stations_data:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations.append(station_dict)

    return jsonify(stations)

#tobs
@app.route("/api/v1.0/tobs")
def tobs():
    #Query of dates, precipitations, and temperature observations
    tobs_data = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= dt.date(2016,8,23)).\
        filter(Measurement.date <= dt.date(2017,8,23)).all()

    # Dict of data to jsonify
    tobs = list(np.ravel(tobs_data))
    return jsonify(tobs)

#start/end
@app.route("/api/v1.0/temp/2016/2017")
def year():
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= dt.date(2016,8,23)).\
        filter(Measurement.date <= dt.date(2017,8,23)).all()
    list_data = list(np.ravel(data))
    return jsonify(list_data)

if __name__ == '__main__':
    app.run()