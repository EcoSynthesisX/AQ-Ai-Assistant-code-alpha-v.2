from flask import Flask, render_template, request
import requests
import os
import openai

app = Flask(__name__)

# Set your API keys as environment variables for security
google_api_key = os.environ.get('GOOGLE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

openai.api_key = openai_api_key

def get_air_quality(location):
    url = f"https://example.com/airquality?location={location}&key={google_api_key}"  # Update with real API URL
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extract the necessary data, e.g., AQI
        aqi = data["results"]["aqi"]  # Update this path according to the actual response structure
        return aqi
    else:
        return "Data not available"

def generate_recommendations(aqi):
    response = openai.Completion.create(
      engine="text-davinci-003",  # Or whichever model you're using
      prompt=f"The air quality index (AQI) is {aqi}. Provide health recommendations.",
      temperature=0.7,
      max_tokens=100,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    return response.choices[0].text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def report():
    location = request.form['location']
    aqi = get_air_quality(location)
    recommendations = generate_recommendations(aqi)
    return render_template('report.html', location=location, air_quality=f"AQI: {aqi}", recommendations=recommendations)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
