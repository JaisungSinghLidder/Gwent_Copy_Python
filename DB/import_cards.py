import sqlite3
import json

# Connect to the existing database
conn = sqlite3.connect('cards.db')
c = conn.cursor()

# Load cards from JSON file
with open(r"C:\Users\jaisu\PycharmProjects\GwentClone\Card_Space\cards.json", 'r') as file:
    cards = json.load(file)

# Insert each card into the database
for card in cards:
    c.execute("""
        INSERT INTO cards (
            card_name,
            faction,
            row,
            base_strength,
            current_strength,
            card_type,
            ability,
            is_affected_by_weather,
            is_affected_by_horn
        ) VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        card['card_name'],
        card['faction'],
        card['row'],
        card['base_strength'],
        card['current_strength'],
        card['card_type'],
        card['ability'],
        False,  # Default value for is_affected_by_weather
        False   # Default value for is_affected_by_horn
    ))

# Commit and close
conn.commit()
conn.close()
