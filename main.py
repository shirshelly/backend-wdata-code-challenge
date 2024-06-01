import os
import re

from flask import Flask, request, jsonify
from database import ingest_data, query
import json

app = Flask(__name__)


def check_condition(temperature, precipitation, condition):
    if condition == "veryHot" and float(temperature) > 30:
        return True
    if condition == "rainyAndCold" and float(temperature) < 10 and float(precipitation) > 0.5:
        return True
    return False


# validate that temperature, precipitation are numbers and condition is 'veryHot' or 'rainyAndCold'. return o if
# input is valid, 1 otherwise
def validate_input(lon, lat, condition):
    if condition != "veryHot" and condition != "rainyAndCold":
        return 1
    if not bool(re.match(r'^[-+]?[0-9]*\.?[0-9]+$', lon)):
        return 1
    if not bool(re.match(r'^[-+]?[0-9]*\.?[0-9]+$', lat)):
        return 1
    return 0


# Error handling
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="An unexpected error occurred. Please try again later."), 500


@app.route('/weather/insight')
def get_data():
    lon = request.args.get("lon")
    lat = request.args.get("lat")
    condition = request.args.get("condition")

    if lon and lat and condition:
        if validate_input(lon, lat, condition):
            return jsonify(
                error="temperature should be a number, precipitation should be a number, condition should be "
                      "'veryHot' or 'rainyAndCold'"), 400

        records = query(lon, lat)
        results = []
        for record in records:
            forcast_time = record[3]
            temperature = record[4]
            precipitation = record[5]
            condition_met = check_condition(temperature, precipitation, condition)
            results.append({"forecastTime": forcast_time, "conditionMet": condition_met})
        return json.dumps(results, indent=2), 200
    return jsonify(error="Usage: https://backend-wdata-code-challenge-shirsh.onrender.com/weather/insight?condition={"
                         "condition}&lat={lat}&lon={lon}"), 400


if __name__ == '__main__':
    ingest_data()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
