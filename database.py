import sqlite3

DB_FILE = 'weather_data.db'
TABLE_NAME = "weather"


# Get record based on Lon and Lat
def query(lon, lat):
    connection = sqlite3.connect(DB_FILE)
    c = connection.cursor()
    c.execute("SELECT * FROM " + TABLE_NAME + " WHERE Longitude=" + lon + " AND Latitude=" + lat)
    records = c.fetchall()
    connection.close()
    return records
