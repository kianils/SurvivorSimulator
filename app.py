from flask import Flask, request, render_template, redirect, url_for
from SurvivorData import fetch_and_process_season_data  # Fetch data from the website
from initializePlayers import initialize_players_from_excel  # Initialize players from Excel
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
    Process the season input from the user, fetch and initialize players.
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
        # Convert the season number to an integer
        season_number = int(season_number)

        # Step 1: Fetch the season data (download Excel file)
        logging.info(f"Fetching data for Season {season_number}...")
        fetch_and_process_season_data(season_number)

        # Step 2: Initialize players from the Excel file
        logging.info(f"Initializing players for Season {season_number}...")
        players = initialize_players_from_excel(season_number)

        # Render the initializePlayer template with player data
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


@app.route('/next', methods=['POST'])
def go_to_next_page():
    """
    Handle the 'Next' button to proceed to the Tribe Sorter page.
    """
    try:
        # You can pass the season number or any required data to the next page
        season_number = request.form.get('season_number')
        return redirect(url_for('tribe_sorter', season_number=season_number))
    except Exception as e:
        logging.error(f"Error moving to next page: {str(e)}")
        return render_template(
            'initializePlayer.html',
            error_message=f"Error moving to the next page: {str(e)}"
        )


@app.route('/tribe_sorter/<int:season_number>')
def tribe_sorter(season_number):
    """
    Render the tribe sorter page for the given season.
    """
    # Here you would load and display players for tribe sorting
    # Logic to fetch players can be added if required
    return render_template('tribeSorter.html', season_number=season_number)


if __name__ == '__main__':
    app.run(debug=True)