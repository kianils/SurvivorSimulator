from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
from SurvivorData import fetch_and_process_season_data  # Import your refactored function

app = Flask(__name__)

@app.route('/')
def homepage():
    # Render the homepage with the form for season input
    return render_template('index.html')

@app.route('/process_season', methods=['POST'])
def process_season():
    season_number = request.form.get('season_number')
    if season_number:
        try:
            # Convert season_number to an integer
            season_number = int(season_number)

            # Process the season number
            result = fetch_and_process_season_data(season_number)

            # Redirect to the initializePlayer page, passing season_number and result as query parameters
            return redirect(url_for('initialize_player', season_number=season_number, result=str(result)))

        except Exception as e:
            # Handle errors and return JSON response
            return jsonify({"error": str(e)}), 500

    # Return error if season_number is invalid
    return jsonify({"error": "Invalid input"}), 400

@app.route('/initializePlayer/<int:season_number>')
def initialize_player(season_number):
    # Retrieve the result passed as a query parameter
    result = request.args.get('result', "No result available")
    
    # Render the initializePlayer.html page with the season number and result
    return render_template('initializePlayer.html', season_number=season_number, result=result)

if __name__ == '__main__':
    app.run(debug=True)