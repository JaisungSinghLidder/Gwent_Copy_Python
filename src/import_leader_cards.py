import sqlite3
import json

#using this file to get previous json file into the database

#just connecting to the previous database
conn = sqlite3.connect('leader_cards.db')
c = conn.cursor()

#loading cards from JSON file
with open (r"C:\Users\jaisu\PycharmProjects\GwentClone\Card_Space\leader_cards.json", 'r') as file:
    leader_cards = json.load(file)

# Inserting each card into the database
for card in leader_cards:
    c.execute("""
        INSERT INTO leader_cards (
            leader_name,
            leader_ability,
            faction
        ) VALUES (?,?,?)
    """, (
        card['leader_name'],
        card['leader_ability'],
        card['faction'],
    ))

#now closing it

conn.commit()
conn.close()
