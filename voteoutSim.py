import networkx as nx
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

def build_tribe_graph(tribe):
    """
    Build a social graph for the tribe.
    :param tribe: A Tribe object.
    :return: A NetworkX Graph object.
    """
    graph = nx.Graph()

    # Add nodes for each player
    for player in tribe.players:
        graph.add_node(player.name, player=player)

    # Add edges based on pairwise features
    for i, player1 in enumerate(tribe.players):
        for j, player2 in enumerate(tribe.players):
            if i < j:
                # Calculate edge weight
                social_skill_diff = abs(player1.socialSkill - player2.socialSkill)
                morale_diff = abs(player1.morale - player2.morale)
                weight = 10 - (social_skill_diff + morale_diff)
                weight = max(weight, 1)  # Ensure positive weight

                # Add edge
                graph.add_edge(player1.name, player2.name, weight=weight)

    return graph

def find_weakest_player(tribe_graph):
    """
    Find the weakest player in the tribe based on the weakest relationship.
    :param tribe_graph: A NetworkX Graph representing the tribe's social relationships.
    :return: The name of the weakest player.
    """
    # Find the edge with the smallest weight
    weakest_edge = min(tribe_graph.edges(data=True), key=lambda edge: edge[2]["weight"])
    weakest_players = [weakest_edge[0], weakest_edge[1]]

    # Evaluate which player contributes the least to the tribe
    player_scores = {
        player: tribe_graph.degree(player, weight="weight") for player in weakest_players
    }
    weakest_player = min(player_scores, key=player_scores.get)

    return weakest_player

def update_alliances(alliances, eliminated_player):
    """
    Update the alliances to remove the eliminated player.
    :param alliances: Dictionary of alliances.
    :param eliminated_player: The player to be removed.
    :return: Updated alliances.
    """
    updated_alliances = {}
    for tribe, tribe_alliances in alliances.items():
        updated_alliances[tribe] = [
            [player for player in alliance if player != eliminated_player]
            for alliance in tribe_alliances
        ]
        # Remove empty alliances
        updated_alliances[tribe] = [alliance for alliance in updated_alliances[tribe] if len(alliance) > 1]
    return updated_alliances

def simulate_tribal_council(tribe):
    """
    Simulate a tribal council to determine the player voted out.
    :param tribe: A Tribe object.
    :return: The name of the player voted out.
    """
    # Build the tribe's social graph
    tribe_graph = build_tribe_graph(tribe)

    # Find the weakest player
    weakest_player_name = find_weakest_player(tribe_graph)

    # Remove the weakest player from the tribe
    weakest_player = next(player for player in tribe.players if player.name == weakest_player_name)
    tribe.players.remove(weakest_player)

    print(f"\n{weakest_player_name} has been voted out from {tribe.name}!")

    # Update tribe stats
    tribe.update_tribe_stats()

    return weakest_player_name

def main():
    # Load tribes from JSON
    tribes_data = load_data_from_json("jsonData/sorted_tribes.json")
    runthrough_data = load_data_from_json("jsonData/Runthroughdata.json")
    alliances_data = load_data_from_json("jsonData/tribe_alliances.json")

    if not tribes_data or not runthrough_data or not alliances_data:
        print("Error: Missing required data. Exiting.")
        return

    # Convert JSON data to Tribe objects
    tribes = []
    for tribe_data in tribes_data:
        players = [
            Player(
                name=player["name"],
                tribe=tribe_data["name"],
                challengeSkill=player["challengeSkill"],
                intelligenceSkill=player["intelligenceSkill"],
                socialSkill=player["socialSkill"],
                luck=player["luck"]
            )
            for player in tribe_data["players"]
        ]
        tribe = Tribe(name=tribe_data["name"], players=players)
        tribe.update_tribe_stats()
        tribes.append(tribe)

    # Get the tribe at tribal council from runthrough data
    latest_round = runthrough_data.get("rounds", [])[-1]
    if not latest_round:
        print("Error: No tribal council round data found.")
        return

    losing_tribe_name = latest_round["losing_tribe"]
    losing_tribe = next((tribe for tribe in tribes if tribe.name == losing_tribe_name), None)

    if not losing_tribe:
        print(f"Error: Losing tribe '{losing_tribe_name}' not found in data.")
        return

    # Simulate tribal council for the losing tribe
    print(f"\nSimulating tribal council for {losing_tribe.name}:")
    voted_out = simulate_tribal_council(losing_tribe)

    # Add the eliminated player to the Runthroughdata.json
    runthrough_data.setdefault("eliminated", []).append(voted_out)
    with open("jsonData/Runthroughdata.json", "w") as file:
        json.dump(runthrough_data, file, indent=4)
    print(f"Updated Runthroughdata.json with eliminated player: {voted_out}")

    # Update alliances
    updated_alliances = update_alliances(alliances_data, voted_out)
    with open("jsonData/tribe_alliances.json", "w") as file:
        json.dump(updated_alliances, file, indent=4)
    print(f"Updated tribe_alliances.json by removing player: {voted_out}")

    # Save updated tribes data back to JSON
    updated_tribes = []
    for tribe in tribes:
        updated_tribes.append({
            "name": tribe.name,
            "players": [
                {
                    "name": player.name,
                    "challengeSkill": player.challengeSkill,
                    "intelligenceSkill": player.intelligenceSkill,
                    "socialSkill": player.socialSkill,
                    "luck": player.luck,
                    "immunityWins": player.immunityWins,
                    "votesReceived": player.votesReceived,
                    "morale": player.morale,
                }
                for player in tribe.players
            ]
        })

    with open("jsonData/sorted_tribes.json", "w") as file:
        json.dump(updated_tribes, file, indent=4)
    print(f"Updated sorted_tribes.json by removing player: {voted_out}")

if __name__ == "__main__":
    from class_Definitions.tribeClass import Tribe
    from class_Definitions.playerClass import Player
    main()