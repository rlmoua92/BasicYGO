"""
This module contains the Deck class used to represent a player's deck in a 
Duel.
"""

from random import shuffle

from decklist import DeckList


class Deck:

    """
    This is a class to represent a represent a player's deck in a Duel.

    Attributes:
        deck (DeckList): The list of cards used to create a Deck.
        deck_count (int): The count of cards currently in a Deck.
    """
    
    def __init__(self, decklist):
        """The constructor for the DeckList class.

        Parameters:
            decklist (DeckList): The list of cards used to create a Deck.
        """
        self.deck = decklist.to_list()
        self.deck_count = len(self.deck)

    def __len__(self):
        """Returns the count of cards currently in a Deck."""
        return self.deck_count

    def shuffle(self):
        """Shuffles the order of cards in a Deck."""
        shuffle(self.deck)

    def draw(self, number=1):
        """Removes number amount of cards from the front of a Deck and
        returns a list containing those Card instances.
        """
        cards = []
        for i in range(number):
            cards.append(self.deck.pop(0))
        self.deck_count -= number
        return cards

    def add_card_to_deck(self, card, location="TOP"):
        """Inserts the Card instance card either to the front or back of a 
        Deck depending on location."""
        if location == "TOP":
            self.deck.insert(0, card)
        elif location == "BOTTOM":
            self.deck.append(card)
        self.deck_count += 1

    def is_empty(self):
        """Returns if the count of cards currently in a Deck is 0."""
        return self.deck_count == 0