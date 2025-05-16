class Card:
    #This is the constructor for the class
    #ability = None is just a default constructor class
    def __init__(self, card_name, faction, row, strength, card_type, ability = None):
        #attributes are set to the parameterized values
        self.card_name = card_name
        self.faction = faction
        self.row = row
        self.strength = strength
        self.ability = ability
        self.card_type = card_type

    #returning the strength value
    def get_strength(self):
        return self.strength

    #returning the row
    def get_row(self):
        return self.row

    #returning the card type
    def get_card_type(self):
        return self.card_type

    #set the strength value
    def set_strength(self,value):
        self.strength = value

    #returning the faction
    def get_faction(self):
        return self.faction

    #returning the ability
    def get_ability(self):
        return self.ability







