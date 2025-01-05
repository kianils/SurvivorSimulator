import os
from google_images_search import GoogleImagesSearch


# Use your provided API Key and CSE ID directly
API_KEY = 'AIzaSyBnoi1Tjie0WPNRnAbI_i272L3STP8Scns'
CSE_ID = '70e9be109311c416f'

# Initialize Google Images Search
gis = GoogleImagesSearch(API_KEY, CSE_ID)


def fetch_player_images(player_names, season_number):
    """
    Fetches player images from Google Images and saves them locally.

    Args:
        player_names (list): A list of player names to search for.
        season_number (int): The season number for saving images in a specific folder.

    Returns:
        dict: A dictionary mapping player names to their image file paths or None if not found.
    """
    # Create a directory to store images for the given season
    image_dir = f"static/player_images/season_{season_number}"
    os.makedirs(image_dir, exist_ok=True)  # Ensure the directory exists

    player_images = {}

    for name in player_names:
        try:
            # Define search parameters for Google Images
            search_params = {
                'q': f"{name} Survivor",
                'num': 1,  # Fetch only 1 image
                'safe': 'medium',  # Safe search setting
                'fileType': 'jpg|png',  # Image file types
                'imgType': 'photo'  # Search for photos only
            }

            # Perform the Google Images search
            gis.search(search_params)

            # Download the first image result
            for image in gis.results():
                image_path = os.path.join(image_dir, f"{name.replace(' ', '_')}.jpg")
                image.download(image_dir)  # Download the image to the directory
                os.rename(image.path, image_path)  # Rename the downloaded image to match the player's name
                player_images[name] = image_path
                break  # Exit after the first result is processed

        except Exception as e:
            # Handle errors gracefully and log them
            print(f"Error fetching image for {name}: {e}")
            player_images[name] = None  # Set None for players whose images couldn't be fetched

    return player_images