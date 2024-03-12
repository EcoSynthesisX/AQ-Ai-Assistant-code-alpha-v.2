from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def report():
    location = request.form['location']
    # Simulated air quality data for demonstration
    air_quality = "Moderate"  # This would be replaced with real data from an API
    recommendations = "Limit outdoor activities."  # This would be dynamic based on the air quality

    return render_template('report.html', location=location, air_quality=air_quality, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
