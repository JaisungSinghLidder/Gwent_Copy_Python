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
    card_type: str
    ability: str







