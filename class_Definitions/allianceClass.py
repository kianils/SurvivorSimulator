import numpy as np

class Player:
    def __init__(self, name, tribe, gender, challengeSkill, intelligenceSkill, socialSkill, luck=None):
        # Core attributes
        self.name = name
        self.tribe = tribe
        self.gender = gender
        self.challengeSkill = challengeSkill
        self.intelligenceSkill = intelligenceSkill
        self.socialSkill = socialSkill
        self.luck = luck if luck else np.random.uniform(0.1, 1.0)  # Random luck value between 0.1 and 1.0

        # Immunity status
        self.holdsHiddenImmunityIdol = False
        self.holdsIndividualImmunity = False

        # Tribal council record
        self.votesReceived = 0
        self.immunityWins = 0
        self.isEliminated = False
        self.isJuryMember = False

        # Dynamic attributes for alliances
        self.alliances = []  # List of alliances the player is part of
        self.trust_levels = {}  # Trust levels with other players (dict with Player -> trust value)
        self.morale = np.random.uniform(0.1, 1.0)  # Random morale value at the start

    def join_alliance(self, alliance):
        """
        Join an alliance and update the player's trust levels for other alliance members.
        """
        if alliance not in self.alliances:
            self.alliances.append(alliance)
            for player in alliance.players:
                if player != self:  # Initialize trust levels with other members
                    self.trust_levels[player] = np.random.uniform(0.5, 1.0)

    def leave_alliance(self, alliance):
        """
        Leave an alliance and clear trust levels related to that alliance.
        """
        if alliance in self.alliances:
            self.alliances.remove(alliance)
            for player in alliance.players:
                if player in self.trust_levels:
                    del self.trust_levels[player]

    def betray_alliance(self, alliance, target_player):
        """
        Betray an alliance by voting against a member or acting against its interests.
        """
        if alliance in self.alliances and target_player in alliance.players:
            # Decrease trust with all members in the alliance
            for player in alliance.players:
                if player in self.trust_levels:
                    self.trust_levels[player] *= 0.5  # Halve trust levels as a consequence of betrayal
            # Leave the alliance after betrayal
            self.leave_alliance(alliance)
            print(f"{self.name} has betrayed the {alliance.name} and voted against {target_player.name}!")

    def update_trust(self, other_player, change):
        """
        Update the trust level for a specific player dynamically.
        :param other_player: Player whose trust level is updated
        :param change: Amount to increase or decrease trust (-1.0 to 1.0)
        """
        if other_player not in self.trust_levels:
            self.trust_levels[other_player] = np.random.uniform(0.5, 1.0)  # Initialize trust if not present
        self.trust_levels[other_player] = np.clip(self.trust_levels[other_player] + change, 0.0, 1.0)

    def most_trusted_member(self):
        """
        Identify the most trusted member in the player's alliances.
        """
        if not self.trust_levels:
            return None
        return max(self.trust_levels, key=self.trust_levels.get)

    def least_trusted_member(self):
        """
        Identify the least trusted member in the player's alliances.
        """
        if not self.trust_levels:
            return None
        return min(self.trust_levels, key=self.trust_levels.get)

    def __str__(self):
        """
        String representation of the player's data.
        """
        alliances = [alliance.name for alliance in self.alliances]
        return (f"Player: {self.name}, Tribe: {self.tribe}, Gender: {self.gender}, "
                f"Challenge Skill: {self.challengeSkill}, Intelligence Skill: {self.intelligenceSkill}, "
                f"Social Skill: {self.socialSkill}, Luck: {self.luck:.2f}, Morale: {self.morale:.2f}, "
                f"Holds Hidden Immunity Idol: {self.holdsHiddenImmunityIdol}, Holds Individual Immunity: {self.holdsIndividualImmunity}, "
                f"Votes Received: {self.votesReceived}, Immunity Wins: {self.immunityWins}, "
                f"Is Eliminated: {self.isEliminated}, Is Jury Member: {self.isJuryMember}, "
                f"Alliances: {alliances}")