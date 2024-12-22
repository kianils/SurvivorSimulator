import json
import networkx as nx
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

def create_social_graph(tribes):
    """
    Create a social graph for players within each tribe.
    :param tribes: List of Tribe objects.
    :return: A dictionary of tribe names mapped to their respective social graphs.
    """
    tribe_graphs = {}

    for tribe in tribes:
        # Initialize a graph for this tribe
        graph = nx.Graph()

        # Add players as nodes
        for player in tribe.players:
            graph.add_node(player.name, player=player)

        # Add edges between players in the same tribe
        for i, player1 in enumerate(tribe.players):
            for j, player2 in enumerate(tribe.players):
                if i < j:  # Avoid duplicate edges
                    # Calculate relationship weight
                    social_similarity = (player1.socialSkill + player2.socialSkill) / 2
                    morale_similarity = abs(player1.morale - player2.morale)
                    weight = social_similarity - morale_similarity + np.random.uniform(-1, 1)
                    weight = max(weight, 1)  # Ensure the weight is positive

                    # Add edge to the graph
                    graph.add_edge(player1.name, player2.name, weight=weight)

        # Store the graph for this tribe
        tribe_graphs[tribe.name] = graph

    return tribe_graphs

def form_alliances_from_graph(graph, weight_threshold=5):
    """
    Form alliances from a social graph by clustering strong relationships.
    :param graph: NetworkX graph representing social relationships.
    :param weight_threshold: Minimum weight for strong relationships.
    :return: List of alliances (as lists of player names).
    """
    alliances = []
    visited = set()

    for node in graph.nodes:
        if node not in visited:
            # Find all nodes connected to this node with strong relationships
            alliance = []
            for neighbor in graph.neighbors(node):
                if graph[node][neighbor]['weight'] >= weight_threshold:
                    alliance.append(neighbor)

            # Add the current node to the alliance
            alliance.append(node)
            visited.update(alliance)

            # Only add alliances with more than one player
            if len(alliance) > 1:
                alliances.append(alliance)

    return alliances

# Example Usage
if __name__ == "__main__":
    # Load tribes from JSON
    tribes = load_tribes_from_json("jsonData/sorted_tribes.json")
    if not tribes:
        print("Error: No tribes loaded. Exiting.")
        exit()

    # Create social graphs for each tribe
    tribe_graphs = create_social_graph(tribes)

    # Form alliances and display them
    for tribe_name, graph in tribe_graphs.items():
        print(f"Alliances in {tribe_name}:")
        alliances = form_alliances_from_graph(graph)
        for i, alliance in enumerate(alliances):
            print(f"  Alliance {i+1}: {alliance}")