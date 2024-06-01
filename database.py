import os
import sqlite3
import pandas as pd

db_file = 'weather_data.db'
def convert_inch_to_mm(df):
    df['Precipitation Rate in/hr'] = df['Precipitation Rate in/hr'] * 25.4
    df.rename(columns={'Precipitation Rate in/hr': 'Precipitation Rate mm/hr'}, inplace=True)


def convert_fahrenheit_to_celsius(df):
    df['Temperature Fahrenheit'] = (df['Temperature Fahrenheit'] - 32) * (5 / 9)
    df.rename(columns={'Temperature Fahrenheit': 'Temperature Celsius'}, inplace=True)


def ingest_data():
    # Delete the file if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
    connection = sqlite3.connect(db_file)
    data_folder = "./data"
    for data_file in os.listdir(data_folder):
        df = pd.read_csv(data_folder + '/' + data_file)
        if "Precipitation Rate in/hr" in df:
            convert_inch_to_mm(df)
        if "Temperature Fahrenheit" in df:
            convert_fahrenheit_to_celsius(df)
        df.to_sql('weather', connection, if_exists="append")
    connection.close()


def query(lon, lat):
    connection = sqlite3.connect(db_file)
    c = connection.cursor()
    c.execute("SELECT * FROM weather WHERE Longitude=" + lon + " AND Latitude=" + lat)
    records = c.fetchall()
    connection.close()
    return records
