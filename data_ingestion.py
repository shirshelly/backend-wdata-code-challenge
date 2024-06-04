import os
import pandas as pd
import sqlite3
from database import DB_FILE, TABLE_NAME


def convert_inch_to_mm(df):
    df['Precipitation Rate in/hr'] = df['Precipitation Rate in/hr'] * 25.4
    df.rename(columns={'Precipitation Rate in/hr': 'Precipitation Rate mm/hr'}, inplace=True)


def convert_fahrenheit_to_celsius(df):
    df['Temperature Fahrenheit'] = (df['Temperature Fahrenheit'] - 32) * (5 / 9)
    df.rename(columns={'Temperature Fahrenheit': 'Temperature Celsius'}, inplace=True)


# Insert the data from the CSV files in the 'data' folder into the database
def ingest_data(data_folder):
    # Delete the file if it exists
    # if os.path.exists(DB_FILE):
    #     os.remove(DB_FILE)
    connection = sqlite3.connect(DB_FILE)
    for data_file in os.listdir(data_folder):
        df = pd.read_csv(data_folder + '/' + data_file)
        # Convert precipitation rate from inch to mm if necessary
        if "Precipitation Rate in/hr" in df:
            convert_inch_to_mm(df)
        # Convert precipitation rate from Fahrenheit to Celsius if necessary
        if "Temperature Fahrenheit" in df:
            convert_fahrenheit_to_celsius(df)
        # Add file data to table
        df.to_sql(TABLE_NAME, connection, if_exists="append")
    connection.close()


if __name__ == '__main__':
    data_folder = "./data"
    ingest_data(data_folder)
