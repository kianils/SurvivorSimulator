import requests
from bs4 import BeautifulSoup
import os
import json


def fetch_and_process_season_data(season_number):
    """
    Fetches and processes Survivor season data for the given season number.
    Saves the season data to an Excel file and updates Runthroughdata.json.
    """
    base_url = "https://www.truedorktimes.com/survivor/boxscores/data.htm"

    try:
        # Fetch the main page containing all links
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the Google Sheets link for the given season
        season_link = None
        all_rows = soup.find_all('tr')  # Table rows containing season data
        for row in all_rows:
            # Match the specific season number in the row
            if f"S{season_number}" in row.text:
                # Find the link in the right column (Google Sheets link)
                link = row.find('a', href=True, text=lambda x: "data" in x.lower())
                if link:
                    season_link = link['href']
                break

        if not season_link:
            raise ValueError(f"No Google Sheets link found for Season {season_number}. Data may not be available.")

        print(f"Google Doc Link found for Season {season_number}: {season_link}")

        # Save the data to an Excel file
        os.makedirs("excel_data", exist_ok=True)
        save_path = f"excel_data/survivor_season_{season_number}_data.xlsx"
        download_google_doc_as_export(season_link, save_path, export_format="xlsx")

        # Save season number to JSON
        os.makedirs("json_data", exist_ok=True)
        json_save_path = "json_data/Runthroughdata.json"
        with open(json_save_path, "w") as json_file:
            json.dump({"season_number": season_number}, json_file)

        print(f"Season data saved successfully for season {season_number}.")
        return f"Season data saved for season {season_number}."

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Network error occurred: {e}")
    except Exception as e:
        raise ValueError(f"An error occurred while processing season {season_number}: {e}")


def download_google_doc_as_export(doc_url, save_path, export_format="xlsx"):
    """
    Downloads a Google Doc and saves it as an Excel file.
    """
    if "docs.google.com" in doc_url:
        try:
            # Extract the document ID from the Google Doc URL
            doc_id = doc_url.split('/d/')[1].split('/')[0]
            export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format={export_format}"
            response = requests.get(export_url, timeout=10)
            response.raise_for_status()

            # Save the exported file
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"File saved successfully at {save_path}.")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error downloading Google Doc: {e}")
    else:
        raise ValueError("Invalid Google Doc URL.")


# Example standalone usage
if __name__ == "__main__":
    season_number = 6  # Replace with the desired season number
    try:
        result = fetch_and_process_season_data(season_number)
        print(result)
    except Exception as e:
        print(f"Error: {e}")