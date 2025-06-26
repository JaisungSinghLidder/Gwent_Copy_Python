import json
import sqlite3
from Card_Space.Card import Card
from Card_Space.Leader import Leader
import random

class CardLoader:


    #OLD JSON IMPLEMENTATION
    @staticmethod
    def load_card_from_json(path:str) -> list[Card]:
        with open(path, "r") as f:
            data = json.load(f)
        return [Card(**item) for item in data]

    @staticmethod
    def load_leaders_from_json(path: str) -> list[Leader]:
        with open(path, "r") as f:
            data = json.load(f)
        return [Leader(**item) for item in data]

    @staticmethod
    def load_deck_from_json(path: str, faction: str,  deck_size: int = 20) -> list[Card]:
        cards = CardLoader.load_card_from_json(path)

        faction_cards = [card for card in cards if
                         card.faction == faction.lower().strip() or card.faction == "neutral"]

        cards = random.sample(faction_cards, deck_size)

        return cards


    #NEW SQLlite3 IMPLEMENTATION
    @staticmethod
    def load_card_from_db(db_path: str, faction: str, deck_size: int = 20) -> list[Card]:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        faction = faction.lower().strip()

        c.execute("""
            SELECT card_name, faction, row, base_strength, current_strength, card_type, ability
            FROM cards
            WHERE LOWER(faction) = ? OR LOWER(faction) = 'neutral'
        """, (faction,))

        rows = c.fetchall()
        conn.close()

        if len(rows) < deck_size:
            raise ValueError(f"Not enough cards to build a deck of size {deck_size}. Found {len(rows)}.")

        selected_rows = random.sample(rows, deck_size)

        cards = [Card(
            card_name = row[0],
            faction = row[1],
            row = row[2],
            base_strength = row[3],
            current_strength = row[4],
            card_type = row[5],
            ability = row[6]
        ) for row in selected_rows]

        return cards

    @staticmethod
    def load_leader_card_from_db(db_path: str) -> list[Leader]:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute("SELECT leader_name, leader_ability, faction FROM leader_cards")
        rows = c.fetchall()

        leader_cards = [Leader(
            leader_name = row[0],
            leader_ability = row[1],
            faction = row[2]
        ) for row in rows]

        conn.close()

        return leader_cards


