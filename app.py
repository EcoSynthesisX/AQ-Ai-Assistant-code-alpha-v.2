from flask import Flask, render_template, request
import requests
import os
import openai
import traceback

app = Flask(__name__)

# Assuming you've set these environment variables in Heroku or another hosting service
google_api_key = os.environ.get('GOOGLE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

openai.api_key = openai_api_key

def get_air_quality(lat, lon):
    try:
        url = f"https://maps.googleapis.com/maps/api/airquality/v1/currentAirQuality?location={lat},{lon}&key={google_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Extract the AQI; adjust based on actual data and pollutant of interest
            aqi = data["data"]["indexes"]["baqi"]["value"]  # Adjust this based on your needs and the API's response structure
            aqi_description = data["data"]["indexes"]["baqi"]["category"]  # Example, adjust as needed
            return aqi, aqi_description
        else:
            print(f"Failed to fetch AQI: {response.status_code}")
            return None, "Data not available"
    except Exception as e:
        print(f"Error fetching AQI data: {e}")
        traceback.print_exc()
        return None, "Error occurred while fetching data"

def generate_recommendations(aqi_description):
    try:
        prompt = f"The air quality is described as '{aqi_description}'. What precautions should be taken?"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        traceback.print_exc()
        return "Could not generate recommendations due to an error."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def report():
    # This needs to be adjusted to how you plan to obtain lat and lon (e.g., form input, geolocation API)
    lat = request.form.get('latitude')
    lon = request.form.get('longitude')
    aqi, aqi_description = get_air_quality(lat, lon)
    if aqi:
        recommendations = generate_recommendations(aqi_description)
        air_quality = f"AQI: {aqi}, {aqi_description}"
    else:
        recommendations = "Could not fetch air quality data."
        air_quality = aqi_description
    return render_template('report.html', location=f"{lat}, {lon}", air_quality=air_quality, recommendations=recommendations)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
