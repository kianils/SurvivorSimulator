import json
import numpy as np
from class_Definitions.tribeClass import Tribe
from class_Definitions.playerClass import Player


def load_tribes_from_json(file_path):
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


def adjust_tribe_stats(tribe, performance):
    if performance == "win":
        tribe.morale = min(tribe.morale + np.random.uniform(0.1, 0.3), 10)  # Boost morale
        tribe.cohesion = min(tribe.cohesion + np.random.uniform(0.1, 0.2), 10)  # Slight improvement in cohesion
    elif performance == "lose":
        tribe.morale = max(tribe.morale - np.random.uniform(0.1, 0.3), 0)  # Reduce morale
        tribe.cohesion = min(tribe.cohesion + np.random.uniform(0.2, 0.4), 10)  # Improve cohesion for recovery


def calculate_tribe_score(tribe, challenge_weights, environment_modifier=0):
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

    highlighted = np.random.choice(individual_scores, size=min(2, len(individual_scores)), replace=False)
    highlighted_bonus = sum(np.random.uniform(-0.3, 0.5) * score for score in highlighted)

    environment_bonus = environment_modifier * np.random.uniform(-0.3, 0.3) * base_score
    luck_factor = np.random.uniform(0.9, 1.1)

    return (base_score + highlighted_bonus + environment_bonus) * luck_factor


def simulate_challenge(tribes, round_number, previous_losses=None):
    if previous_losses is None:
        previous_losses = {tribe.name: 0 for tribe in tribes}

    challenge_types = ["physical", "puzzle", "social", "balanced"]
    challenge_type = np.random.choice(challenge_types)

    weights = {
        "physical": {"strength": 0.6, "morale": 0.2, "cohesion": 0.2},
        "puzzle": {"strength": 0.2, "morale": 0.3, "cohesion": 0.3, "intelligence": 0.2},
        "social": {"strength": 0.3, "morale": 0.4, "cohesion": 0.3},
        "balanced": {"strength": 0.4, "morale": 0.3, "cohesion": 0.3},
    }

    print(f"\nRound {round_number} Challenge Type: {challenge_type.title()}")

    scores = {}
    for tribe in tribes:
        environment_modifier = np.random.choice([-1, 0, 1])
        scores[tribe.name] = calculate_tribe_score(tribe, weights[challenge_type], environment_modifier)

        if previous_losses[tribe.name] > 1:
            fatigue_penalty = np.random.uniform(0.05, 0.15) * scores[tribe.name]
            scores[tribe.name] -= fatigue_penalty

    losing_tribe_name = min(scores, key=scores.get)

    print("\nChallenge Results:")
    for tribe_name, score in scores.items():
        print(f"{tribe_name}: {score:.2f}")
    print(f"Losing Tribe: {losing_tribe_name}")

    for tribe in tribes:
        if tribe.name == losing_tribe_name:
            adjust_tribe_stats(tribe, "lose")
            previous_losses[tribe.name] += 1
        else:
            adjust_tribe_stats(tribe, "win")

    write_runthrough_data(round_number, losing_tribe_name)
    return losing_tribe_name, previous_losses


def simulate_full_season(tribes, total_rounds=10):
    previous_losses = {tribe.name: 0 for tribe in tribes}

    for round_number in range(1, total_rounds + 1):
        losing_tribe_name, previous_losses = simulate_challenge(tribes, round_number, previous_losses)

    print("\nFinal Results:")
    for tribe_name, losses in previous_losses.items():
        print(f"{tribe_name} lost {losses} challenges.")


if __name__ == "__main__":
    tribes = load_tribes_from_json("jsonData/sorted_tribes.json")
    if not tribes:
        print("Error: No tribes loaded.")
        exit()

    simulate_full_season(tribes, total_rounds=1)