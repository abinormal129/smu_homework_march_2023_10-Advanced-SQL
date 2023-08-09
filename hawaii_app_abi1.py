# Import the dependencies
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from flask import Flask, jsonify
import json

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
hawaii_engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f"""<h1>Available Routes:<h1><br/>
        <h4><a href="/api/v1.0/precipitation" target="_blank">Past Year Precipitation Analysis</a><h4><br/>
        <h4><a href="/api/v1.0/stations" target="_blank">List of Observation Station</a><h4><br/>
        <h4><a href="/api/v1.0/tobs" target="_blank">Past Year Temperatures</a><h4><br/>
        <h4><a href="/api/v1.0/2016-08-23" target="_blank">Min, Max, and Avg Temps: 2016-08-23</a><h4><br/>
        <h4><a href="/api/v1.0/2016-08-23/2016-09-23" target="_blank">Mix, Max, and Avg Temps: from 2016-08-23 to 2016-09-23</a><h4><br/>
        """
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    """Get 12-Month Precipitation Analysis"""
    prcp_year_query = text("""
                SELECT
                    date,
                    prcp
                FROM
                    measurement
                WHERE
                    date >= '2016-08-23';
            """)

    prcp_year_df = pd.read_sql(prcp_year_query, hawaii_engine)
    data = json.loads(prcp_year_df.to_json(orient="records"))
    return(data)

@app.route("/api/v1.0/stations")
def stations():
    """Get List of Stations"""
    station_query = text("""
                SELECT
                    name,
                    station
                FROM
                    station
                GROUP BY
                    station;
            """)

    station_df = pd.read_sql(station_query, hawaii_engine)
    data = json.loads(station_df.to_json(orient="records"))
    return(data)

@app.route("/api/v1.0/tobs")
def temps():
    """Get Past Year of Temps for Most Active Station"""
    temp_year_query = text("""
                SELECT
                    date,
                    station,
                    tobs as temp
                FROM
                    measurement
                WHERE
                    date >= '2016-08-23'
                    and station = 'USC00519281'
                ORDER BY
                    date ASC;
            """)

    temp_year_df = pd.read_sql(temp_year_query, hawaii_engine)
    data = json.loads(temp_year_df.to_json(orient="records"))
    return(data)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    """Calculate min, max, avg temps from user start date"""
    temp_start_query = text(f"""
                SELECT
                    station,
                    ROUND(avg(tobs), 2) as temp_avg,
                    max(tobs) as temp_max,
                    min(tobs) as temp_min
                FROM
                    measurement
                WHERE
                    date >= '{start}';

            """)

    start_df = pd.read_sql(temp_start_query, hawaii_engine)
    data = json.loads(start_df.to_json(orient="records"))
    return(data)

@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end):
    """Calculate min, max, avg temps in user date range"""
    temp_range_query = text(f"""
                SELECT
                    station,
                    ROUND(avg(tobs), 2) as temp_avg,
                    max(tobs) as temp_max,
                    min(tobs) as temp_min                    
                FROM
                    measurement
                WHERE
                    date >= '{start}'
                    and date <= '{end}';

            """)

    temp_range_df = pd.read_sql(temp_range_query, hawaii_engine)
    data = json.loads(temp_range_df.to_json(orient="records"))
    return(data)

# run the website
if __name__ == '__main__':
    app.run(debug=True)
