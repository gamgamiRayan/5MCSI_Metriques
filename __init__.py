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
    return render_template("hello.html")

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
    response = requests.get(url)
    data = response.json()

    # Extraire les minutes de chaque commit
    minutes_list = []
    for item in data:
        try:
            date_str = item["commit"]["author"]["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minutes_list.append(date_obj.minute)
        except:
            continue

    # Compter les commits par minute
    minute_counts = Counter(minutes_list)
    minute_data = sorted(minute_counts.items())  # [(minute, count), ...]

    return render_template("commits.html", data=minute_data)

if __name__ == "__main__":
    app.run(debug=True)
