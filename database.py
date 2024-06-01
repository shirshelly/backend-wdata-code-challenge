import os
import sqlite3
import pandas as pd

db_file = 'weather_data.db'
table_name = "weather"


def convert_inch_to_mm(df):
    df['Precipitation Rate in/hr'] = df['Precipitation Rate in/hr'] * 25.4
    df.rename(columns={'Precipitation Rate in/hr': 'Precipitation Rate mm/hr'}, inplace=True)


def convert_fahrenheit_to_celsius(df):
    df['Temperature Fahrenheit'] = (df['Temperature Fahrenheit'] - 32) * (5 / 9)
    df.rename(columns={'Temperature Fahrenheit': 'Temperature Celsius'}, inplace=True)


# Insert the data from the CSV files in the 'data' folder into the database
def ingest_data():
    # Delete the file if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
    connection = sqlite3.connect(db_file)
    data_folder = "./data"
    for data_file in os.listdir(data_folder):
        df = pd.read_csv(data_folder + '/' + data_file)
        # Convert precipitation rate from inch to mm if necessary
        if "Precipitation Rate in/hr" in df:
            convert_inch_to_mm(df)
        # Convert precipitation rate from Fahrenheit to Celsius if necessary
        if "Temperature Fahrenheit" in df:
            convert_fahrenheit_to_celsius(df)
        # Add file data to table
        df.to_sql(table_name, connection, if_exists="append")
    connection.close()


# Get record based on Lon and Lat
def query(lon, lat):
    connection = sqlite3.connect(db_file)
    c = connection.cursor()
    c.execute("SELECT * FROM " + table_name + " WHERE Longitude=" + lon + " AND Latitude=" + lat)
    records = c.fetchall()
    connection.close()
    return records
