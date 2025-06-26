class Faction:

    def __init__(self, faction_name, leader, faction_ability, deck, ai_strat):

        self.faction_name = faction_name
        self.leader = leader
        self.faction_ability = faction_ability
        self.deck = deck

        if self.faction_name == "northern realms":
            self.ai_strat = "balanced"
        elif self.faction_name == "nilfgaard":
            self.ai_strat = "spy-heavy"
        elif self.faction_name == "monsters":
            self.ai_strat = "swarm"
        elif self.faction_name == "scoia'tael":
            self.ai_strat = "agile"
        elif self.faction_name ==  "skellige":
            self.ai_strat = "resurrection"



























