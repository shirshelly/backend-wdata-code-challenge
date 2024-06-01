import os

from flask import Flask, request
from database import ingest_data, query
import json

app = Flask(__name__)


def check_condition(temperature, precipitation, condition):
    if condition == "veryHot" and float(temperature) > 30:
        return True
    if condition == "rainyAndCold" and float(temperature) < 10 and float(precipitation) > 0.5:
        return True
    return False


@app.route('/weather/insight')
def get_data():
    lon = request.args.get("lon")
    lat = request.args.get("lat")
    condition = request.args.get("condition")

    if lon and lat and condition:
        records = query(lon, lat)
        results = []
        for record in records:
            forcast_time = record[3]
            temperature = record[4]
            precipitation = record[5]
            condition_met = check_condition(temperature, precipitation, condition)
            results.append({"forecastTime": forcast_time, "conditionMet": condition_met})

        return json.dumps(results, indent=2), 200
    return 'error', 404


if __name__ == '__main__':
    ingest_data()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

