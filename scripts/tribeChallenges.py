import json
import numpy as np
from class_Definitions.tribeClass import Tribe
from class_Definitions.playerClass import Player

def load_tribes_from_json(file_path):
    """
    Load tribes and players from a JSON file.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            tribes = []
            for tribe_data in data:
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
                tribe = Tribe(name=tribe_data["name"], players=players)
                tribe.update_tribe_stats()
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
    Write the challenge result (losing tribe and round) to a JSON file.
    """
    try:
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if "season_number" not in data:
            print("Error: 'season_number' not found in the JSON file.")
            return

        if "rounds" not in data:
            data["rounds"] = []

        data["rounds"].append({
            "round": round_number,
            "losing_tribe": losing_tribe_name
        })

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Round {round_number}: Losing tribe '{losing_tribe_name}' logged.")
    except Exception as e:
        print(f"Error writing runthrough data: {e}")

def calculate_tribe_score(tribe, challenge_weights, environment_modifier=0):
    """
    Calculate the score for a tribe based on stats and individual player contributions.
    """
    base_score = (
        tribe.tribe_strength * challenge_weights["strength"] +
        tribe.morale * challenge_weights["morale"] +
        tribe.cohesion * challenge_weights["cohesion"]
    )

    individual_scores = []
    for player in tribe.players:
        player_score = (
            player.challengeSkill * challenge_weights["strength"] +
            player.socialSkill * challenge_weights["cohesion"] +
            player.intelligenceSkill * challenge_weights.get("intelligence", 0)
        )
        individual_scores.append(player_score)

    # Highlight 2 players randomly and add bonuses
    highlighted = np.random.choice(individual_scores, size=min(2, len(individual_scores)), replace=False)
    highlighted_bonus = sum(np.random.uniform(-0.5, 1.5) * score for score in highlighted)

    # Random event buff/debuff (environmental factor)
    environment_bonus = environment_modifier * np.random.uniform(-0.2, 0.3) * base_score

    # Luck factor
    luck_factor = np.random.uniform(0.85, 1.15)

    return (base_score + highlighted_bonus + environment_bonus) * luck_factor

def simulate_challenge(tribes, round_number):
    """
    Simulate a Survivor challenge and determine which tribe loses.
    """
    challenge_types = ["physical", "puzzle", "social", "balanced"]
    challenge_type = np.random.choice(challenge_types)

    weights = {
        "physical": {"strength": 0.7, "morale": 0.2, "cohesion": 0.1},
        "puzzle": {"strength": 0.1, "morale": 0.2, "cohesion": 0.3, "intelligence": 0.4},
        "social": {"strength": 0.2, "morale": 0.4, "cohesion": 0.4},
        "balanced": {"strength": 0.4, "morale": 0.3, "cohesion": 0.3},
    }

    print(f"\nRound {round_number} Challenge Type: {challenge_type.title()}")

    scores = {}
    for tribe in tribes:
        environment_modifier = np.random.choice([0, 1])  # Random environmental factor applied to some tribes
        scores[tribe.name] = calculate_tribe_score(tribe, weights[challenge_type], environment_modifier)

    losing_tribe_name = min(scores, key=scores.get)

    print("\nChallenge Results:")
    for tribe_name, score in scores.items():
        print(f"{tribe_name}: {score:.2f}")
    print(f"Losing Tribe: {losing_tribe_name}")

    write_runthrough_data(round_number, losing_tribe_name)
    return losing_tribe_name

if __name__ == "__main__":
    tribes = load_tribes_from_json("jsonData/sorted_tribes.json")
    if not tribes:
        print("Error: No tribes loaded.")
        exit()
        
simulate_challenge(tribes, round_number=1)  # Simulate one challenge round