from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Assuming you have set these environment variables in your hosting service
google_api_key = os.environ.get('GOOGLE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

def get_air_quality(lat, lon):
    # Adjust the endpoint URL and parameters according to the Google Air Quality API documentation
    url = f"https://maps.googleapis.com/maps/api/place/airquality/json?location={lat},{lon}&key={google_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        # Make sure to adjust the path according to the actual response structure
        aqi_data = response.json()
        return aqi_data
    else:
        print(f"Failed to fetch AQI: {response.status_code}, {response.text}")
        return None

def generate_advice_with_chatgpt(aqi_data):
    prompt = f"The current Air Quality Index (AQI) is {aqi_data}. What precautions should people take?"
    headers = {'Authorization': f'Bearer {openai_api_key}'}
    data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 150
    }
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    if response.status_code == 200:
        advice = response.json()["choices"][0]["text"].strip()
        return advice
    else:
        print(f"Failed to generate advice: {response.status_code}, {response.text}")
        return "Sorry, I am unable to provide recommendations at the moment."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-advice', methods=['POST'])
def get_advice():
    lat = request.form.get('latitude')
    lon = request.form.get('longitude')
    aqi_data = get_air_quality(lat, lon)
    advice = generate_advice_with_chatgpt(str(aqi_data))
    return jsonify({'advice': advice})

if __name__ == '__main__':
    app.run(debug=True)
