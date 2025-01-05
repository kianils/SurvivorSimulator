# %%
import pandas as pd
import numpy as np
import json
import openpyxl
from class_Definitions.playerClass import Player

# %%
def initialize_players_from_excel(seasonNum):
    """
    Initializes players from the given season, processes data from Excel,
    and returns the updated player list.
    """
    file_path = f"excel_data/survivor_season_{seasonNum}_data.xlsx"
    output_path = f"jsonData/survivor_season_{seasonNum}_players.json"

    try:
        # Load the Excel data
        df = pd.read_excel(file_path)
        print("DataFrame Loaded:", df.head())
    except FileNotFoundError:
        raise Exception(f"Excel file not found for season {seasonNum}.")
    
    # Adjust column names and ensure required columns
    df.columns = df.columns.str.strip()
    required_columns = ['ChW', 'TotCh', 'VFB', 'SurvSc', 'VAP', 'InICA', 'InICW']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise Exception(f"Missing required columns: {missing_columns}")

    # Filter valid rows
    df = df.dropna(subset=['ChW', 'TotCh'])

    # Initialize players
    players = []
    processed_names = set()
    for _, row in df.iterrows():
        name = row.get('Pre-table 1', None)
        if pd.isna(name) or name in processed_names:
            continue
        processed_names.add(name)

        try:
            challenge_wins = float(row.get('ChW', 0))
            challenge_appearances = float(row.get('TotCh', 0))
            votes_for_bootee = float(row.get('VFB', 0))
            survival_score = float(row.get('SurvSc', 0))
            votes_against_player = float(row.get('VAP', 0))
            immunity_wins = float(row.get('InICA', 0)) + float(row.get('InICW', 0))
        except ValueError:
            continue

        # Calculate skills
        challenge_skill = round((challenge_wins / challenge_appearances) * 10, 2) if challenge_appearances > 0 else 1
        social_skill = round((votes_for_bootee / (votes_for_bootee + 1)) * 10, 2) if votes_for_bootee > 0 else 1
        intelligence_skill = round(survival_score, 2)
        luck = round(np.random.uniform(0.5, 1.0), 2)
        morale = round(np.random.uniform(0.5, 1.0), 2)

        player = {
            "name": name,
            "tribe": "Unknown",  # Tribe assignment logic can go here
            "challengeSkill": challenge_skill,
            "intelligenceSkill": intelligence_skill,
            "socialSkill": social_skill,
            "luck": luck,
            "immunityWins": immunity_wins,
            "votesReceived": votes_against_player,
            "morale": morale,
        }
        players.append(player)

    # Handle duplicate removal and NaN cleanup
    try:
        with open(output_path, "r") as file:
            existing_players = json.load(file)
            existing_names = {player["name"] for player in existing_players}
            players = [
                player for player in players
                if player["name"] not in existing_names and
                   not any(pd.isna(player[field]) for field in ["challengeSkill", "intelligenceSkill", "socialSkill", "luck", "immunityWins", "votesReceived", "morale"])
            ]
            players.extend(existing_players)
    except (FileNotFoundError, json.JSONDecodeError):
        players = [
            player for player in players
            if not any(pd.isna(player[field]) for field in ["challengeSkill", "intelligenceSkill", "socialSkill", "luck", "immunityWins", "votesReceived", "morale"])
        ]

    # Save updated player data
    with open(output_path, "w") as file:
        json.dump(players, file, indent=4)

    print(f"Initialized players saved to: {output_path}")
    return players