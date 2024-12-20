import requests
from bs4 import BeautifulSoup
import json
import os
seasonNum=0


# Function to ensure the input is a valid season number and fetch the webpage
def get_valid_season_and_fetch_page():
    global seasonNum  # Declare the global variable
    while True:
        seasonNum = input("What season number would you like to use as data for Survivor? ").strip()
        if seasonNum.isdigit():
            url = f"https://www.truedorktimes.com/survivor/boxscores/s{seasonNum}.htm"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"Successfully fetched data for season {seasonNum}.")
                    return seasonNum, response
                else:
                    print(f"Failed to fetch the webpage for season {seasonNum} (Status Code: {response.status_code}). Try again.")
            except requests.RequestException as e:
                print(f"Error fetching the webpage: {e}. Try again.")
        else:
            print("Invalid season number, please enter digits only.")

# Function to download the Google Doc in a specified format
def download_google_doc_as_export(doc_url, save_path, export_format="xlsx"):
    """
    Downloads the Google Doc in the specified format.

    Args:
        doc_url (str): The URL of the Google Doc.
        save_path (str): The file path to save the document.
        export_format (str): The export format (e.g., 'xlsx', 'pdf', 'csv').
    """
    try:
        # Modify the Google Doc link to an export URL
        if "docs.google.com" in doc_url:
            doc_id = doc_url.split('/d/')[1].split('/')[0]  # Extract Google Doc ID
            export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format={export_format}"

            # Fetch the exported content
            response = requests.get(export_url, timeout=10)
            response.raise_for_status()  # Raise an error for HTTP issues

            # Save the exported file
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"Google Doc successfully saved to: {save_path}")
        else:
            print("Invalid Google Doc URL.")
    except requests.RequestException as e:
        print(f"Error downloading the Google Doc: {e}")

# Get a valid season number and the response
season_number, response = get_valid_season_and_fetch_page()

# Parse the webpage content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the anchor tag containing the Google Doc link
google_doc_link = soup.find('a', href=lambda href: href and "docs.google.com" in href)

# Save the Google Doc if found
if google_doc_link:
    google_doc_url = google_doc_link['href']
    print("Google Doc Link found:", google_doc_url)
      # Ensure the directory exists
    os.makedirs("excel_data", exist_ok=True)
    
    save_path = f"excel_data/survivor_season_{season_number}_data.xlsx"  # Save as Excel file
    download_google_doc_as_export(google_doc_url, save_path, export_format="xlsx")
else:
    print("Google Doc Link not found on the webpage.")

## export season number to json
# Export season number to JSON
season_data = {"season_number": season_number}

# Ensure the directory exists
os.makedirs("json_data", exist_ok=True)

json_save_path = f"jsonData/Runthroughdata.json"
with open(json_save_path, "w") as json_file:
    json.dump(season_data, json_file)

print(f"Season number successfully saved to: {json_save_path}")