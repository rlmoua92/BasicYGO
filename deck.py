from random import shuffle

from decklist import DeckList


class Deck:

    def __init__(self, decklist):
        self.deck = decklist.to_list()
        self.deck_count = len(self.deck)

    def __len__(self):
        return self.deck_count

    def shuffle(self):
        shuffle(self.deck)

    def draw(self, number=1):
        cards = []
        for i in range(number):
            cards.append(self.deck.pop(0))
        self.deck_count -= number
        return cards

    def add_card_to_deck(self, card, position="TOP"):
        if position == "TOP":
            self.deck.insert(0, card)
        elif position == "BOTTOM":
            self.deck.append(card)
        self.deck_count += 1

    def is_empty(self):
        return self.deck_count == 0