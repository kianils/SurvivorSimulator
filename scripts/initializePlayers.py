# %%
import pandas as pd
import numpy as np
import json
import openpyxl
from class_Definitions.playerClass import Player

# %%

def get_season_number(json_file_path):
    """
    Extract the season number from the given JSON file.
    :param json_file_path: Path to the JSON file.
    :return: The season number as a string or None if not found.
    """
    try:
        # Open the JSON file and load its content
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Extract the season number
        if "season_number" in data:
            return data["season_number"]
        else:
            print("Error: 'season_number' not found in the JSON file.")
            return None
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        print("Error: The JSON file is corrupted or not valid JSON.")
        return None


# %%
seasonNum = get_season_number("jsonData/Runthroughdata.json")
if not seasonNum:
    print("Error: Season number not found. Exiting.")
    exit()

file_path = f"excel_data/survivor_season_{seasonNum}_data.xlsx"


# %%


# Load the data from the Excel file
try:
    df = pd.read_excel(file_path)
    print("DataFrame Loaded:")
    print(df.head())  # Display the first few rows for debugging
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()

# Adjust column names if needed
df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
print("Adjusted Column Names:", df.columns)

# Drop rows with missing critical stats
df = df.dropna(subset=['ChW', 'ChA'])
print("Filtered DataFrame:")
print(df)

# List to store initialized players
players = []

# Set to track already processed player names
processed_names = set()

# Extract Player Data
for _, row in df.iterrows():
    name = row.get('Unnamed: 0', None)  # Adjust column name if needed
    if pd.isna(name) or name in processed_names:
        continue  # Skip if the name is NaN or already processed

    # Mark the player as processed
    processed_names.add(name)

    # Extract stats
    challenge_wins = row['ChW']
    challenge_appearances = row['ChA']
    votes_for_bootee = row.get('VFB', 0)
    survival_score = row.get('SurvSc', 0)
    votes_against_player = row.get('VAP', 0)
    immunity_wins = row.get('InICA', 0) + row.get('InICW', 0)

    # Calculate skills
    challenge_skill = round((challenge_wins / challenge_appearances) * 10, 2) if challenge_appearances > 0 else 1
    social_skill = round((votes_for_bootee / (votes_for_bootee + 1)) * 10, 2) if votes_for_bootee > 0 else 1
    intelligence_skill = round(survival_score, 2)
    luck = round(np.random.uniform(0.5, 1.0), 2)
    morale = round(np.random.uniform(0.5, 1.0), 2)

    # Create a Player object
    player = {
        "name": name,
        "tribe": "Unknown",  # To be assigned dynamically later
        "challengeSkill": challenge_skill,
        "intelligenceSkill": intelligence_skill,
        "socialSkill": social_skill,
        "luck": luck,
        "immunityWins": immunity_wins,
        "votesReceived": votes_against_player,
        "morale": morale,
    }

    # Add to players list
    players.append(player)

# Output Initialized Players
print(f"Total Players Initialized: {len(players)}")
print("Saving players to JSON file...")

# Save all players to a JSON file
output_path = f"jsonData/survivor_season_{seasonNum}_players.json"
with open(output_path, "w") as file:
    json.dump(players, file, indent=4)

print(f"Initialized players saved to: {output_path}")
# %%