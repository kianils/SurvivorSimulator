import json

def clear_json_file(file_path, empty_structure):
    """
    Clear the contents of a JSON file by writing an empty structure.
    :param file_path: Path to the JSON file.
    :param empty_structure: The structure to write to the file (e.g., empty dict or list).
    """
    try:
        with open(file_path, "w") as file:
            json.dump(empty_structure, file, indent=4)
        print(f"Cleared data in {file_path}")
    except Exception as e:
        print(f"Error clearing {file_path}: {e}")

def clear_all_jsons():
    """
    Clear all relevant JSON files in the simulation.
    """
    # Define the paths to the JSON files
    files_to_clear = {
        "jsonData/Runthroughdata.json": {"season_number": "", "rounds": [], "eliminated": []},
        "jsonData/tribe_alliances.json": {},
        "jsonData/sorted_tribes.json": []
    }

    # Clear each file
    for file_path, empty_structure in files_to_clear.items():
        clear_json_file(file_path, empty_structure)

if __name__ == "__main__":
    clear_all_jsons()