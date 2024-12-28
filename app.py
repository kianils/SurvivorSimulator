from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def homepage():
    return render_template('index.html')

# API route to fetch Survivor data
@app.route('/fetch-survivor-data', methods=['POST'])
def fetch_survivor_data():
    season_num = request.json.get('season_number')
    if not season_num or not season_num.isdigit():
        return jsonify({"error": "Invalid season number"}), 400

    url = f"https://www.truedorktimes.com/survivor/boxscores/s{season_num}.htm"
    try:
        # Fetch the webpage
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the Google Doc link
        google_doc_link = soup.find('a', href=lambda href: href and "docs.google.com" in href)
        if google_doc_link:
            google_doc_url = google_doc_link['href']
            # Save the Google Doc
            save_path = f"excel_data/survivor_season_{season_num}_data.xlsx"
            os.makedirs("excel_data", exist_ok=True)
            download_google_doc_as_export(google_doc_url, save_path, export_format="xlsx")
            return jsonify({"message": "Data successfully fetched and saved!", "save_path": save_path})

        return jsonify({"error": "Google Doc link not found on the webpage"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to download the Google Doc as an Excel file
def download_google_doc_as_export(doc_url, save_path, export_format="xlsx"):
    if "docs.google.com" in doc_url:
        doc_id = doc_url.split('/d/')[1].split('/')[0]
        export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format={export_format}"
        response = requests.get(export_url, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            file.write(response.content)

if __name__ == '__main__':
    app.run(debug=True)