from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def report():
    location = request.form['location']
    air_quality = "Moderate"  # Placeholder for real data
    recommendations = "Limit outdoor activities."  # Placeholder for real advice
    return render_template('report.html', location=location, air_quality=air_quality, recommendations=recommendations)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
