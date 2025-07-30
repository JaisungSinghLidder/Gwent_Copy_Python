from dataclasses import dataclass, field


#using dataclasses since this is just an information class
#using this gets rid of some of the boilerplate code
#Since it already creates comparisons
#now I am going to base it off strength right now to keep the code easier for my AI
#it probably won't be the smartest yet, but I can deal with that for now until I find another way to do it.

@dataclass()
class Card:

    card_name: str
    faction: str
    row: str
    #this is going to be their base strength
    base_strength: int
    #meanwhile this will be the strength that will be changed by differing conditions
    current_strength: int
    #adding these flags for weather and horn
    is_affected_by_weather: bool = field(compare = False)
    is_affected_by_horn: bool = field(compare = False)
    card_type: str
    ability: str

    def clone(self):
        return Card(
            card_name=self.card_name,
            faction= self.faction,
            row = self.row,
            base_strength= self.base_strength,
            current_strength= self.current_strength,
            is_affected_by_weather= self.is_affected_by_weather,
            is_affected_by_horn= self.is_affected_by_horn,
            card_type= self.card_type,
            ability = self.ability 
        )






