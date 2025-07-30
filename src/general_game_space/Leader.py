from dataclasses import dataclass

from src.cards.Card import Card

#just holding the data, so we are going to make them dataclass
@dataclass
class Leader:

    def __init__(self, leader_name: str, leader_ability: str, faction: str):
        self.leader_name = leader_name
        self.leader_ability = leader_ability
        self.faction = faction


    def clone(self):

        return Leader(

            leader_name = self.leader_name,
            leader_ability = self.leader_ability,
            faction= self.faction

        )
