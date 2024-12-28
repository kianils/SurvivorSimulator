from flask import Flask, request, render_template, jsonify
import os
from SurvivorData import fetch_and_process_season_data  # Import your refactored function

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/process_season', methods=['POST'])
def process_season():
    season_number = request.form.get('season_number')
    if season_number:
        try:
            season_number = int(season_number)
            result = fetch_and_process_season_data(season_number)
            return jsonify({"message": "Data processed successfully!", "result": result})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(debug=True)