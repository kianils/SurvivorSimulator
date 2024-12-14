import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website
url = "https://www.truedorktimes.com/survivor/boxscores/index.htm"

# Fetch the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the webpage!")
else:
    print(f"Failed to fetch webpage. Status code: {response.status_code}")
    exit()