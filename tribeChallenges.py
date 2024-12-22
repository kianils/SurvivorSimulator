import json
import numpy as np
from class_Definitions.tribeClass import Tribe
from class_Definitions.playerClass import Player

def load_tribes_from_json(file_path):
    """
    Load tribes and players from a JSON file.
    :param file_path: Path to the JSON file.
    :return: List of Tribe objects.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            tribes = []
            for tribe_data in data:
                # Create Player objects for each player in the tribe
                players = [
                    Player(
                        name=player["name"],
                        tribe=tribe_data["name"],
                        challengeSkill=player["challengeSkill"],
                        intelligenceSkill=player["intelligenceSkill"],
                        socialSkill=player["socialSkill"],
                        luck=player["luck"]
                    ) for player in tribe_data["players"]
                ]
                # Create Tribe object
                tribe = Tribe(name=tribe_data["name"], players=players)
                tribe.update_tribe_stats()  # Ensure stats are updated
                tribes.append(tribe)
            return tribes
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print("Error: The JSON file is corrupted or not valid JSON.")
        return []

def write_runthrough_data(round_number, losing_tribe_name, file_path="jsonData/Runthroughdata.json"):
    """
    Write the challenge result (losing tribe and round) to a JSON file without overwriting the season number.
    :param round_number: The current round number.
    :param losing_tribe_name: The name of the tribe that lost the challenge.
    :param file_path: Path to the JSON file.
    """
    try:
        # Load existing data if the file exists
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Ensure "season_number" key is preserved
        if "season_number" not in data:
            print("Error: 'season_number' not found in the JSON file.")
            return

        # Initialize "rounds" key if it doesn't exist
        if "rounds" not in data:
            data["rounds"] = []

        # Append the new result to the "rounds" key
        data["rounds"].append({
            "round": round_number,
            "losing_tribe": losing_tribe_name
        })

        # Write back to the file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Round {round_number}: Losing tribe '{losing_tribe_name}' logged.")
    except Exception as e:
        print(f"Error writing runthrough data: {e}")

def simulate_challenge(tribes, round_number, challenge_type="balanced"):
    """
    Simulate a Survivor challenge and determine which tribe loses.
    
    :param tribes: List of Tribe objects.
    :param round_number: Current round number.
    :param challenge_type: Type of challenge ("physical", "puzzle", "social", or "balanced").
    :return: The losing Tribe object.
    """
    weights = {
        "physical": {"strength": 0.7, "morale": 0.2, "cohesion": 0.1},
        "puzzle": {"strength": 0.1, "morale": 0.2, "cohesion": 0.7},
        "social": {"strength": 0.2, "morale": 0.4, "cohesion": 0.4},
        "balanced": {"strength": 0.4, "morale": 0.3, "cohesion": 0.3},
    }
    
    if challenge_type not in weights:
        raise ValueError("Invalid challenge type. Choose from 'physical', 'puzzle', 'social', or 'balanced'.")
    
    challenge_weights = weights[challenge_type]
    scores = {}
    for tribe in tribes:
        random_factor = np.random.uniform(0.8, 1.2)
        score = (
            tribe.tribe_strength * challenge_weights["strength"] +
            tribe.morale * challenge_weights["morale"] +
            tribe.cohesion * challenge_weights["cohesion"]
        ) * random_factor
        scores[tribe.name] = score
    
    losing_tribe_name = min(scores, key=scores.get)
    losing_tribe = next(tribe for tribe in tribes if tribe.name == losing_tribe_name)
    
    print("\nChallenge Results:")
    for tribe_name, score in scores.items():
        print(f"{tribe_name}: {score:.2f}")
    print(f"Losing Tribe: {losing_tribe.name}")

    # Write the result to Runthroughdata.json
    write_runthrough_data(round_number, losing_tribe_name)

    return losing_tribe

# Example Usage
if __name__ == "__main__":
    tribes = load_tribes_from_json("jsonData/sorted_tribes.json")
    if not tribes:
        print("Error: No tribes loaded.")
        exit()

    # Simulate one challenge round
    simulate_challenge(tribes, round_number=1, challenge_type="balanced")