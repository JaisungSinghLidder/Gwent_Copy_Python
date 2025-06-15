import sqlite3

# Connect to database

conn = sqlite3.connect('cards.db')

# cursor

c = conn.cursor()

#creating the cards table
c.execute("""CREATE TABLE IF NOT EXISTS cards (
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_name TEXT, 
    faction TEXT,
    row TEXT, 
    base_strength INTEGER,
    current_strength INTEGER,
    card_type TEXT,
    ability TEXT
 
)



""")

#commiting the table
conn.commit()
#closing the table
conn.close()
