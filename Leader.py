from dataclasses import dataclass

from Card_Space.Card import Card

#just holding the data, so we are going to make them dataclass
@dataclass
class Leader:

    def __init__(self, leader_name, leader_ability, faction):
        self.leader_name = leader_name
        self.leader_ability = leader_ability
        self.faction = faction
