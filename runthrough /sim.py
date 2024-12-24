import os
import json
import subprocess
import time

def run_script(script_name):
    """
    Run a Python script using the subprocess module with animated output.
    :param script_name: Name of the script to execute.
    """
    try:
        print(f"\n🔄 Running {script_name}...")
        time.sleep(1)  # Adding a slight delay for better animation
        subprocess.run(f"python {script_name}", shell=True, check=True)
        print(f"✅ {script_name} completed successfully.")
        time.sleep(0.5)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error occurred while running {script_name}: {e}")
        raise

def load_json(file_path):
    """
    Load data from a JSON file.
    :param file_path: Path to the JSON file.
    :return: Parsed JSON data.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"⚠️ Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"⚠️ Error: JSON file at {file_path} is not valid.")
        return None

def save_json(data, file_path):
    """
    Save data to a JSON file.
    :param data: Data to save.
    :param file_path: Path to the JSON file.
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"💾 Saved updates to {file_path}")
    except Exception as e:
        print(f"⚠️ Error saving JSON file at {file_path}: {e}")

def count_remaining_players(tribes):
    """
    Count the total number of players remaining across all tribes.
    :param tribes: List of tribes.
    :return: Total number of players.
    """
    return sum(len(tribe["players"]) for tribe in tribes)

def merge_tribes(tribes, runthrough_data_path):
    """
    Merge all tribes into a single tribe.
    :param tribes: List of tribes.
    :param runthrough_data_path: Path to the Runthroughdata.json file.
    """
    print("\n🔄 Merging all tribes into one...")
    time.sleep(1)

    merged_tribe = {
        "name": "Merged Tribe",
        "players": []
    }

    # Add all players from each tribe into the merged tribe
    for tribe in tribes:
        merged_tribe["players"].extend(tribe["players"])

    # Update Runthroughdata.json with merged tribe
    runthrough_data = load_json(runthrough_data_path)
    if not runthrough_data:
        runthrough_data = {"season_number": "", "rounds": [], "eliminated": []}

    runthrough_data["merged_tribe"] = merged_tribe
    save_json(runthrough_data, runthrough_data_path)

    print("✅ Merged tribe created and saved in Runthroughdata.json.")
    time.sleep(0.5)

def main():
    # Paths to JSON files
    sorted_tribes_path = "jsonData/sorted_tribes.json"
    runthrough_data_path = "jsonData/Runthroughdata.json"

    print("🏝️ Starting Survivor Simulation...\n")
    time.sleep(1)

    # Run initial tribe sorting (only once)
    if not os.path.exists(sorted_tribes_path) or not load_json(sorted_tribes_path):
        print("🔄 Running initial tribe sorting...")
        run_script("tribeSorter.py")
        print("✅ Tribe sorting completed.")

    # Ensure the initial state is correct
    tribes = load_json(sorted_tribes_path)
    if not tribes:
        print("❌ Error: Failed to load tribes data. Exiting.")
        return

    # Run initial simulation steps
    print("\n🎬 Initializing first simulation steps...\n")
    time.sleep(1)
    run_script("tribeChallenges.py")  # Run initial challenge
    run_script("alliance_sim.py")     # Simulate initial alliances
    run_script("voteoutSim.py")      # Simulate vote-out
    run_script("updateAlliance.py")  # Update alliances

    # Main simulation loop
    while True:
        # Reload the updated tribes data
        tribes = load_json(sorted_tribes_path)
        if not tribes:
            print("❌ Error: Failed to load tribes data. Exiting.")
            return

        remaining_players = count_remaining_players(tribes)
        print(f"\n🔢 Remaining players: {remaining_players}")
        time.sleep(1)

        if remaining_players <= 11:
            print("\n⚡ Less than 11 players remaining. Merging tribes!\n")
            time.sleep(1)
            break

        # Run the simulation steps
        run_script("tribeChallenges.py")  # Run challenge
        run_script("voteoutSim.py")      # Simulate vote-out
        run_script("updateAlliance.py")  # Update alliances

    # Reload tribes for final merge
    tribes = load_json(sorted_tribes_path)
    if tribes:
        merge_tribes(tribes, runthrough_data_path)
        print("\n🎉 Simulation complete. Tribes merged into one. 🏆")
    else:
        print("❌ Error: Failed to load tribes data for merging.")

if __name__ == "__main__":
    main()