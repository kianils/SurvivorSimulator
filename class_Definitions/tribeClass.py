class Tribe:
    def __init__(self, name, players=None):
        """
        Initialize a Tribe object.
        :param name: Name of the tribe.
        :param players: List of Player objects belonging to this tribe (default is None).
        """
        self.name = name  # Tribe name
        self.players = players if players else []  # List of Player objects
        self.update_tribe_stats()  # Initialize tribe stats

    def update_tribe_stats(self):
        """
        Update the tribe's overall stats such as strength, morale, and social cohesion.
        """
        if self.players:
            # Calculate total challenge strength
            self.tribe_strength = sum(player.challengeSkill for player in self.players)

            # Calculate average morale
            self.morale = sum(player.morale for player in self.players) / len(self.players)

            # Calculate average social cohesion (social skill)
            self.cohesion = sum(player.socialSkill for player in self.players) / len(self.players)
        else:
            # Default values for empty tribe
            self.tribe_strength = 0
            self.morale = 0
            self.cohesion = 0

    def add_player(self, player):
        """
        Add a player to the tribe and update stats.
        :param player: Player object to add.
        """
        if player not in self.players:
            self.players.append(player)
            player.tribe = self.name  # Update player's tribe designation
            self.update_tribe_stats()

    def remove_player(self, player):
        """
        Remove a player from the tribe and update stats.
        :param player: Player object to remove.
        """
        if player in self.players:
            self.players.remove(player)
            player.tribe = None  # Clear player's tribe designation
            self.update_tribe_stats()

    def merge_with(self, other_tribe):
        """
        Merge this tribe with another tribe.
        :param other_tribe: Another Tribe object to merge with.
        """
        for player in other_tribe.players:
            self.add_player(player)  # Add players from the other tribe
        other_tribe.players = []  # Clear the other tribe's player list
        other_tribe.update_tribe_stats()

    def __str__(self):
        """
        String representation of the tribe, showing its stats and members.
        """
        player_names = [player.name for player in self.players]
        return (f"Tribe: {self.name}\n"
                f"Members: {', '.join(player_names)}\n"
                f"Total Strength: {self.tribe_strength:.2f}\n"
                f"Average Morale: {self.morale:.2f}\n"
                f"Social Cohesion: {self.cohesion:.2f}")

    def display_members(self):
        """
        Display a detailed breakdown of all members in the tribe.
        """
        for player in self.players:
            print(player)