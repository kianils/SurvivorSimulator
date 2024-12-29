import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_and_process_season_data(season_number):
    url = f"https://www.truedorktimes.com/survivor/boxscores/s{season_number}.htm"
    try:
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
        os.makedirs("json_data", exist_ok=True)
        json_save_path = "json_data/Runthroughdata.json"
        with open(json_save_path, "w") as json_file:
            json.dump({"season_number": season_number}, json_file)
        return f"Season data saved for season {season_number}."
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")

def download_google_doc_as_export(doc_url, save_path, export_format="xlsx"):
    if "docs.google.com" in doc_url:
        doc_id = doc_url.split('/d/')[1].split('/')[0]
        export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format={export_format}"
        response = requests.get(export_url, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            file.write(response.content)
    else:
        raise ValueError("Invalid Google Doc URL.")