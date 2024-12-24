import json

def load_data_from_json(file_path):
    """
    Load data from a JSON file.
    :param file_path: Path to the JSON file.
    :return: Data loaded from the JSON file as a Python object.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print("Error: The JSON file is corrupted or not valid JSON.")
        return None

def update_alliances_after_vote_out(tribes_data, eliminated_player_name):
    """
    Update alliances after a player is voted out.
    :param tribes_data: List of tribes with players.
    :param eliminated_player_name: Name of the eliminated player.
    :return: Updated alliances.
    """
    alliances = load_data_from_json("jsonData/tribe_alliances.json")
    updated_alliances = {}

    for tribe_name, tribe_alliances in alliances.items():
        updated_alliances[tribe_name] = []
        for alliance in tribe_alliances:
            # Remove the eliminated player from alliances
            if eliminated_player_name in alliance:
                alliance.remove(eliminated_player_name)

            # Only keep alliances with more than one member
            if len(alliance) > 1:
                updated_alliances[tribe_name].append(alliance)

    # Save updated alliances
    with open("jsonData/tribe_alliances.json", "w") as file:
        json.dump(updated_alliances, file, indent=4)
    print(f"Updated tribe_alliances.json by removing player: {eliminated_player_name}")

    # Update personal connections (socialSkill and morale adjustments)
    for tribe in tribes_data:
        for player in tribe["players"]:
            if eliminated_player_name in player.get("connections", {}):
                # Penalize morale for betraying a close ally
                player["morale"] -= 0.2
                player["morale"] = max(player["morale"], 0)  # Ensure morale doesn't go below 0

                # Remove connection to eliminated player
                del player["connections"][eliminated_player_name]

    return tribes_data

def save_updated_tribes(tribes_data, file_path="jsonData/sorted_tribes.json"):
    """
    Save updated tribe data to JSON.
    :param tribes_data: List of tribe dictionaries.
    :param file_path: Path to save the updated tribes JSON.
    """
    updated_tribes = []
    for tribe in tribes_data:
        updated_tribes.append({
            "name": tribe["name"],
            "players": [
                {
                    "name": player["name"],
                    "challengeSkill": player["challengeSkill"],
                    "intelligenceSkill": player["intelligenceSkill"],
                    "socialSkill": player["socialSkill"],
                    "luck": player["luck"],
                    "immunityWins": player.get("immunityWins", 0),
                    "votesReceived": player.get("votesReceived", 0),
                    "morale": player["morale"],
                }
                for player in tribe["players"]
            ]
        })

    with open(file_path, "w") as file:
        json.dump(updated_tribes, file, indent=4)
    print(f"Updated sorted_tribes.json by removing player: {file_path}")

def main():
    # Load tribe data
    tribes_data = load_data_from_json("jsonData/sorted_tribes.json")
    runthrough_data = load_data_from_json("jsonData/Runthroughdata.json")

    if not tribes_data or not runthrough_data:
        print("Error: Missing required data. Exiting.")
        return

    # Get the latest eliminated player
    eliminated_players = runthrough_data.get("eliminated", [])
    if not eliminated_players:
        print("Error: No eliminated player data found.")
        return

    # Get the most recent eliminated player
    eliminated_player_name = eliminated_players[-1]
    print(f"Updating alliances and tribes for eliminated player: {eliminated_player_name}")

    # Update alliances and connections
    updated_tribes_data = update_alliances_after_vote_out(tribes_data, eliminated_player_name)

    # Save updated tribes data
    save_updated_tribes(updated_tribes_data)

if __name__ == "__main__":
    main()