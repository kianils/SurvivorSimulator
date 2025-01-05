from flask import Flask, request, render_template, jsonify
from SurvivorData2 import fetch_and_process_season_data  # Import logic to fetch data
from initializePlayers import initialize_players_from_excel  # Import logic to initialize players
import logging

app = Flask(__name__)

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def homepage():
    """
    Render the homepage with a form for entering the season number.
    """
    return render_template('index.html')


@app.route('/process_season', methods=['POST'])
def process_season():
    """
    Processes the season input from the user.
    """
    season_number = request.form.get('season_number')  # Fetch the season number from the form

    # Validate user input
    if not season_number or not season_number.isdigit():
        logging.warning("Invalid input for season number.")
        return render_template(
            'initializePlayer.html',
            season_number=None,
            players=None,
            error_message="Invalid input. Please enter a valid season number."
        )

    try:
        # Convert input to an integer
        season_number = int(season_number)

        # Step 1: Fetch and process the season data (download the Excel file)
        logging.info(f"Fetching data for season {season_number}...")
        fetch_and_process_season_data(season_number)

        # Step 2: Initialize players from the downloaded Excel file
        logging.info(f"Initializing players for season {season_number}...")
        players = initialize_players_from_excel(season_number)

        # Step 3: Render the initializePlayer template directly with player data
        return render_template(
            'initializePlayer.html',
            season_number=season_number,
            players=players,
            error_message=None
        )

    except Exception as e:
        # Log the error for debugging
        logging.error(f"An error occurred while processing season {season_number}: {str(e)}")
        return render_template(
            'initializePlayer.html',
            season_number=season_number,
            players=None,
            error_message=f"An error occurred while processing season {season_number}: {str(e)}"
        )


if __name__ == '__main__':
    app.run(debug=True)