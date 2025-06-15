import sqlite3

# Connect to database

conn = sqlite3.connect('leader_cards.db')

# cursor

c = conn.cursor()

# creating the cards table
c.execute("""CREATE TABLE IF NOT EXISTS leader_cards (
    leader_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    leader_name TEXT,
    leader_ability TEXT,
    faction TEXT
)



""")

# commiting the table
conn.commit()
# closing the table
conn.close()
