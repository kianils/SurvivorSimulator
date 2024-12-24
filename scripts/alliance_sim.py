import pandas as pd
from itertools import combinations
from class_Definitions.tribeClass import Tribe
from class_Definitions.playerClass import Player
import json
import networkx as nx

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

def generate_pairwise_features(tribe):
    if len(tribe.players) < 2:
        return pd.DataFrame()  # Return an empty DataFrame for tribes with less than two players

    player_pairs = list(combinations(tribe.players, 2))
    features = []

    for player1, player2 in player_pairs:
        social_skill_diff = abs(player1.socialSkill - player2.socialSkill)
        morale_diff = abs(player1.morale - player2.morale)
        combined_challenge_skill = (player1.challengeSkill + player2.challengeSkill) / 2
        combined_luck = (player1.luck + player2.luck) / 2

        features.append({
            "player1": player1.name,
            "player2": player2.name,
            "social_skill_diff": social_skill_diff,
            "morale_diff": morale_diff,
            "combined_challenge_skill": combined_challenge_skill,
            "combined_luck": combined_luck,
        })

    return pd.DataFrame(features)

def build_social_graph(pairwise_data):
    graph = nx.Graph()

    for _, row in pairwise_data.iterrows():
        weight = 10 - (row["social_skill_diff"] + row["morale_diff"])
        if weight > 0:
            graph.add_edge(row["player1"], row["player2"], weight=weight)

    return graph

def form_alliances_from_graph(graph, weight_threshold=5):
    alliances = []
    visited = set()

    for node in graph.nodes:
        if node not in visited:
            alliance = []
            for neighbor in graph.neighbors(node):
                if graph[node][neighbor]["weight"] >= weight_threshold:
                    alliance.append(neighbor)

            alliance.append(node)
            visited.update(alliance)

            if len(alliance) > 1:
                alliances.append(alliance)

    return alliances

if __name__ == "__main__":
    tribes = load_tribes_from_json("jsonData/sorted_tribes.json")

    if not tribes:
        print("Error: No tribes loaded. Exiting.")
        exit()

    all_tribe_alliances = {}
    for tribe in tribes:
        pairwise_data = generate_pairwise_features(tribe)
        social_graph = build_social_graph(pairwise_data)
        alliances = form_alliances_from_graph(social_graph, weight_threshold=5)
        all_tribe_alliances[tribe.name] = alliances

        print(f"\nAlliances in {tribe.name}:")
        for i, alliance in enumerate(alliances):
            print(f"  Alliance {i+1}: {alliance}")

    # Save alliances to a JSON file
    with open("jsonData/tribe_alliances.json", "w") as file:
        json.dump(all_tribe_alliances, file, indent=4)