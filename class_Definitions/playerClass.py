import numpy as np 

class Player:
    def __init__(self, name, tribe, gender, challengeSkill, intelligenceSkill, socialSkill, luck=None):
        # Player Attributes
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

        # ML game stats
        self.curr_TribeSize = 0
        self.alliance = None  # Placeholder for alliance class
        self.morale = np.random.uniform(0.1, 1.0)  # Random morale value at the start 

    def feature_vector(self):
        """
        Generate a feature vector for the player.
        """
        return np.array([
            self.challengeSkill, 
            self.intelligenceSkill, 
            self.socialSkill, 
            self.luck, 
            self.morale,
            self.holdsHiddenImmunityIdol,
            self.holdsIndividualImmunity,
            self.votesReceived,
            self.immunityWins,
            self.isEliminated,
            self.isJuryMember,
            self.curr_TribeSize
        ])
    def update_dynamic_context(self, tribe_size=None, alliance_size=None, morale=None, holdsHiddenImmunityIdol=None, holdsIndividualImmunity=None, votesReceived=None, immunityWins=None, isEliminated=None, isJuryMember=None):
        """
        Update dynamic game context variables.
        """
        if tribe_size is not None:
            self.curr_TribeSize = tribe_size
        if alliance_size is not None:
            self.alliance_size = alliance_size
        if morale is not None:
            self.morale = morale
        if holdsHiddenImmunityIdol is not None:
            self.holdsHiddenImmunityIdol = holdsHiddenImmunityIdol
        if holdsIndividualImmunity is not None:
            self.holdsIndividualImmunity = holdsIndividualImmunity
        if votesReceived is not None:
            self.votesReceived = votesReceived
        if immunityWins is not None:
            self.immunityWins = immunityWins
        if isEliminated is not None:
            self.isEliminated = isEliminated
        if isJuryMember is not None:
            self.isJuryMember = isJuryMember

    def update_dynamic_context(self, tribe_size, alliance_size, morale=None):
        """
        Update dynamic game context variables such as tribe size, alliance size, and morale.
        """
        self.tribe_size = tribe_size
        self.alliance_size = alliance_size
        if morale is not None:
            self.morale = morale

    def __str__(self):
                """
                Return a string representation of the player's data.
                """
                return (f"Player: {self.name}, Tribe: {self.tribe}, Gender: {self.gender}, "
                        f"Challenge Skill: {self.challengeSkill}, Intelligence Skill: {self.intelligenceSkill}, "
                        f"Social Skill: {self.socialSkill}, Luck: {self.luck:.2f}, Morale: {self.morale:.2f}, "
                        f"Holds Hidden Immunity Idol: {self.holdsHiddenImmunityIdol}, Holds Individual Immunity: {self.holdsIndividualImmunity}, "
                        f"Votes Received: {self.votesReceived}, Immunity Wins: {self.immunityWins}, "
                        f"Is Eliminated: {self.isEliminated}, Is Jury Member: {self.isJuryMember}, "
                        f"Current Tribe Size: {self.curr_TribeSize}")