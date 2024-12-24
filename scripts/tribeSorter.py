import json
from class_Definitions.playerClass import Player
from class_Definitions.tribeClass import Tribe

def load_players_from_json(file_path):
    """
    Load players from a JSON file.
    :param file_path: Path to the JSON file.
    :return: List of Player objects.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            players = [
                Player(
                    name=player["name"],
                    tribe=player["tribe"],
                    challengeSkill=player["challengeSkill"],
                    intelligenceSkill=player["intelligenceSkill"],
                    socialSkill=player["socialSkill"],
                    luck=player["luck"],
                )
                for player in data
            ]
            for i, player in enumerate(players):
                player.immunityWins = data[i]["immunityWins"]
                player.votesReceived = data[i]["votesReceived"]
                player.morale = data[i]["morale"]
            return players
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print("Error: The JSON file is corrupted or not valid JSON.")
        return []


def manual_sort(players):
    """
    Manually sort players into tribes.
    :param players: List of Player objects.
    :return: List of Tribe objects.
    """
    tribes = {}
    print("\nManual Tribe Sorting:")
    for player in players:
        print(f"Player: {player.name}")
        tribe_name = input("Enter the tribe name for this player: ").strip()
        if tribe_name not in tribes:
            tribes[tribe_name] = Tribe(name=tribe_name)
        tribes[tribe_name].add_player(player)
    return list(tribes.values())


def balanced_sort(players, num_tribes):
    """
    Automatically sort players into balanced tribes.
    :param players: List of Player objects.
    :param num_tribes: Number of tribes to create.
    :return: List of Tribe objects.
    """
    # Sort players by challengeSkill, socialSkill, and intelligenceSkill
    sorted_players = sorted(players, key=lambda p: (p.challengeSkill, p.socialSkill, p.intelligenceSkill), reverse=True)
    
    # Initialize tribes
    tribes = [Tribe(name=f"Tribe {i+1}") for i in range(num_tribes)]

    # Distribute players round-robin to balance skills
    for i, player in enumerate(sorted_players):
        tribes[i % num_tribes].add_player(player)

    return tribes


def save_tribes_to_json(tribes, file_path):
    """
    Save tribes to a JSON file.
    :param tribes: List of Tribe objects.
    :param file_path: Path to the JSON file.
    """
    tribes_data = []
    for tribe in tribes:
        tribe_data = {
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
            ],
            "tribe_strength": tribe.tribe_strength,
            "morale": tribe.morale,
            "cohesion": tribe.cohesion,
        }
        tribes_data.append(tribe_data)

    with open(file_path, "w") as file:
        json.dump(tribes_data, file, indent=4)
    print(f"Tribes saved to: {file_path}")


def main():
    # Load players from JSON
    players = load_players_from_json("jsonData/survivor_season_28_players.json")
    if not players:
        print("Error: No players loaded. Exiting.")
        return

    # Ask user for sorting method
    print("\nHow would you like to sort the tribes?")
    print("1. Manually")
    print("2. Automatically (Balanced Sort)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        # Manual sorting
        tribes = manual_sort(players)
    elif choice == "2":
        # Automatic balanced sorting
        num_tribes = int(input("Enter the number of tribes to create: ").strip())
        tribes = balanced_sort(players, num_tribes)
    else:
        print("Invalid choice. Exiting.")
        return

    # Display tribe compositions and stats
    print("\nFinal Tribes:")
    for tribe in tribes:
        print(tribe)
        tribe.display_members()

    # Save tribes to JSON
    save_tribes_to_json(tribes, "jsonData/sorted_tribes.json")


if __name__ == "__main__":
    main()