import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_and_process_season_data(season_number):
    """
    Fetches and processes the Survivor season data for the given season number.
    Saves the season data to an Excel file and updates Runthroughdata.json.
    """
    url = f"https://www.truedorktimes.com/survivor/boxscores/s{season_number}.htm"
    try:
        # Fetch the webpage
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the Google Doc link
        google_doc_link = soup.find('a', href=lambda href: href and "docs.google.com" in href)
        if not google_doc_link:
            raise ValueError("Google Doc link not found on the webpage.")

        google_doc_url = google_doc_link['href']
        print(f"Google Doc Link found: {google_doc_url}")

        # Save the data to an Excel file
        os.makedirs("excel_data", exist_ok=True)
        save_path = f"excel_data/survivor_season_{season_number}_data.xlsx"
        download_google_doc_as_export(google_doc_url, save_path, export_format="xlsx")

        # Save season number to JSON
        os.makedirs("jsonData", exist_ok=True)
        json_save_path = "jsonData/Runthroughdata.json"
        print(f"Saving season number {season_number} to JSON file at {json_save_path}")

        # Write to the JSON file
        with open(json_save_path, "w") as json_file:
            json.dump({"season_number": str(season_number)}, json_file)  # Ensure season_number is a string

        print(f"Season data saved successfully for season {season_number}.")
        return f"Season data saved for season {season_number}."
    except Exception as e:
        raise ValueError(f"An error occurred while processing season {season_number}: {e}")

def download_google_doc_as_export(doc_url, save_path, export_format="xlsx"):
    """
    Downloads a Google Doc and saves it as an Excel file.
    """
    if "docs.google.com" in doc_url:
        doc_id = doc_url.split('/d/')[1].split('/')[0]
        export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format={export_format}"
        response = requests.get(export_url, timeout=10)
        response.raise_for_status()

        # Save the exported file
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"File saved successfully at {save_path}.")
    else:
        raise ValueError("Invalid Google Doc URL.")