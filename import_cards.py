import sqlite3
import json

#using this file to get previous json file into the database

#just connecting to the previous database
conn = sqlite3.connect('cards.db')
c = conn.cursor()

#loading cards from JSON file
with open (r"C:\Users\jaisu\PycharmProjects\GwentClone\Card_Space\cards.json", 'r') as file:
    cards = json.load(file)

# Inserting each card into the database
for card in cards:
    c.execute("""
        INSERT INTO cards (
            card_name,
            faction,
            row,
            base_strength,
            current_strength,
            card_type,
            ability
        ) VALUES (?,?,?,?,?,?,?)
    """, (
        card['card_name'],
        card['faction'],
        card['row'],
        card['base_strength'],
        card['current_strength'],
        card['card_type'],
        card['ability']
    ))

#now closing it

conn.commit()
conn.close()