import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.get("/live-roe-accepted")
def live_eaton_fire():
    url = "https://jecop-public.usace.army.mil/arcgis/rest/services/USACE_Debris_Parcels_Southern_California_Public/MapServer/0/query?f=json&cacheHint=true&orderByFields=&outFields=*&outStatistics=%5B%7B%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%2C%22statisticType%22%3A%22count%22%7D%5D&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=((ma%20%3D%20%274856DR-CA-COE-SPD-09%27)%20AND%20(event_sub_name%20IN%20(%27Palisades%27%2C%27Eaton%27)))%20AND%20(ma%3D%274856DR-CA-COE-SPD-09%27%20AND%20roe_approved%20IS%20NOT%20NULL)"

    # validating response from url 
    response = requests.get(url, verify=False)

    # error status checker 
    if response.status_code != 200: 
        return jsonify({"error": "Failed to fetch data"}), 500

    data = response.json()

    # extacting live counter of ROE's Accepted from the county 
    # basically the right of entries accepted from the Los Angeles 
    try: 
        value = data["features"][0]["attributes"]["value"]
        return jsonify({"debris_count": value})
    except (KeyError, IndexError):
        return jsonify({"error": "Unexpected response format"}), 500

@app.get("/live-debris-eaton-palisade")
def live_palisade_fire():
# url that has endpoint of live debris removals for the city palisade 
    url = "https://jecop-public.usace.army.mil/arcgis/rest/services/USACE_Debris_Parcels_Southern_California_Public/MapServer/0/query?f=json&cacheHint=true&groupByFieldsForStatistics=event_sub_name&orderByFields=event_sub_name%20ASC&outFields=*&outStatistics=%5B%7B%22onStatisticField%22%3A%22event_sub_name%22%2C%22outStatisticFieldName%22%3A%22count_result%22%2C%22statisticType%22%3A%22count%22%7D%5D&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=((ma%20%3D%20%274856DR-CA-COE-SPD-09%27)%20AND%20(event_sub_name%20IN%20(%27Palisades%27%2C%27Eaton%27)))%20AND%20(ma%3D%274856DR-CA-COE-SPD-09%27)"

    # validating response from url 
    response = requests.get(url, verify=False)

    # error status checker 
    if response.status_code != 200: 
        return jsonify({"error": "Failed to fetch data"}), 500

    data = response.json()

    # extacting live counter of debris that lie within  Eaton and palisade 
    try:
        # Build a map from event_sub_name to count_result
        result_map = {
            feature["attributes"]["event_sub_name"]: feature["attributes"]["count_result"]
            for feature in data["features"]
        }

        # Return both values as a JSON response
        return jsonify({
            "Eaton": result_map.get("Eaton", 0),
            "Palisades": result_map.get("Palisades", 0)
        })

    except (KeyError, IndexError, TypeError):
        return jsonify({"error": "Unexpected response format"}), 500

@app.get("/live-total-signoff")
def final_signoff():
    url = "https://jecop-public.usace.army.mil/arcgis/rest/services/USACE_Debris_Parcels_Southern_California_Public/MapServer/0/query?f=json&cacheHint=true&orderByFields=&outFields=*&outStatistics=%5B%7B%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%2C%22statisticType%22%3A%22count%22%7D%5D&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=((ma%20%3D%20%274856DR-CA-COE-SPD-09%27)%20AND%20(event_sub_name%20IN%20(%27Palisades%27%2C%27Eaton%27)))%20AND%20(fso_pkg_approved%20IS%20NOT%20NULL%20AND%20ma%3D%274856DR-CA-COE-SPD-09%27)"

    # validating response from url 
    response = requests.get(url, verify=False)

    # error status checker 
    if response.status_code != 200: 
        return jsonify({"error": "Failed to fetch data"}), 500

    data = response.json()

    # extacting live counter of ROE's Accepted from the county 
    # basically the right of entries accepted from the Los Angeles 
    try: 
        value = data["features"][0]["attributes"]["value"]
        return jsonify({"total_signoff": value})
    except (KeyError, IndexError):
        return jsonify({"error": "Unexpected response format"}), 500



    
    
