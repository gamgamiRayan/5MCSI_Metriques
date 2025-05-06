from flask import Flask, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen
import requests
from collections import Counter

app = Flask(__name__)

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route("/tawarano/")
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin -> °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/commits/")
def commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    try:
        response = requests.get(url, timeout=15)  # Increased timeout to 15 seconds
        response.raise_for_status()  # Will raise an HTTPError if the status is not 200
        data = response.json()
    except requests.exceptions.Timeout:
        return "<h2>Le serveur GitHub a mis trop de temps à répondre. Veuillez réessayer plus tard.</h2>"
    except requests.exceptions.RequestException as e:
        return f"<h2>Erreur lors de l'accès à l'API GitHub : {e}</h2>"

    minutes_list = []
    for item in data:
        try:
            date_str = item["commit"]["author"]["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minutes_list.append(date_obj.minute)
        except Exception:
            continue

    minute_counts = Counter(minutes_list)
    minute_data = sorted(minute_counts.items())

    return render_template("commits.html", data=minute_data)


if __name__ == "__main__":
    app.run(debug=True)
