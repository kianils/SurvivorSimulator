from flask import Flask, request, render_template, jsonify, redirect, url_for
from initializePlayers import fetch_and_process_season_data  # Import the logic for initializing players

app = Flask(__name__)

@app.route('/')
def homepage():
    # Render the homepage with the form for season input
    return render_template('index.html')

@app.route('/process_season', methods=['POST'])
def process_season():
    # Get the season number from the form input
    season_number = request.form.get('season_number')
    if season_number:
        try:
            # Process the season number
            season_number = int(season_number)  # Convert input to integer
            players = fetch_and_process_season_data(season_number)  # Call your initialization logic

            # Redirect to initialized players page, passing the player data
            return render_template(
                'initializePlayer.html',
                season_number=season_number,
                players=players
            )
        except Exception as e:
            # Handle any errors that occur during player initialization
            return jsonify({"error": str(e)}), 500

    # If no season number is provided, return an error
    return jsonify({"error": "Invalid input. Please enter a valid season number."}), 400

if __name__ == '__main__':
    app.run(debug=True)