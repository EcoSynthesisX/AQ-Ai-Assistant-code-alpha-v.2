from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# API keys set as environment variables for security
google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

def get_lat_lon(location_name):
    """Converts location name to latitude and longitude using Google Maps Geocoding API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location_name}&key={google_maps_api_key}"
    response = requests.get(url)
    if response.status_code == 200 and response.json()['results']:
        result = response.json()['results'][0]['geometry']['location']
        return result['lat'], result['lng']
    else:
        return None, None

def get_air_quality(lat, lon):
    """Fetches air quality data based on latitude and longitude. Adjust this function based on the real air quality API you're using."""
    # Hypothetical air quality API endpoint; replace with the actual one you plan to use
    air_quality_url = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={google_maps_api_key}"
    response = requests.get(air_quality_url)
    if response.status_code == 200:
        # Adjust the parsing based on the actual response structure of the air quality API
        aqi_data = response.json()  # Example; adjust accordingly
        return aqi_data
    return "Data not available"

def generate_advice_with_chatgpt(location_name, aqi_data):
    """Generates advice using OpenAI's ChatGPT-4 based on air quality data."""
    prompt = f"Given the air quality data {aqi_data} for {location_name}, what advice would you offer?"
    
    headers = {'Authorization': f'Bearer {openai_api_key}'}
    data = {
        "model": "gpt-4",  # Specify using GPT-4
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    if response.status_code == 200:
        advice = response.json()["choices"][0]["text"].strip()
        return advice
    else:
        return "Unable to generate recommendations at this time."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-advice', methods=['POST'])
def get_advice():
    location_name = request.form.get('location')
    lat, lon = get_lat_lon(location_name)
    if lat is None or lon is None:
        advice = "Could not find the specified location."
    else:
        aqi_data = get_air_quality(lat, lon)
        advice = generate_advice_with_chatgpt(location_name, aqi_data)
    return jsonify({'advice': advice})

if __name__ == '__main__':
    app.run(debug=True)
