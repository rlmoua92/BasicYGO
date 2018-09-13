"""
This module contains the Player class used to represent a player in a Duel.
"""

from card import Card, Monster


class Player:

    """
    This is a class to represent a player in a Duel. 

    Attributes:
        id (int): The Player's id.
        hand (list): The Player's hand.
        gy (list): The Player's graveyard.
        deck (Deck): The Player's deck.
        field (Field): The Player's field.
        lp (int):The Player's lifepoints.
        can_summon (bool): Whether the Player can summon or not.
    """

    def __init__(self, id, hand, gy, deck, field, lp=8000):
        """The constructor for the Player class.

        Parameters:
            id (int): The Player's id.
            hand (list): The Player's hand.
            gy (list): The Player's graveyard.
            deck (Deck): The Player's deck.
            field (Field): The Player's field.
            lp (int):The Player's lifepoints. Defaults to 8000.
        """
        self.id = id
        self.hand = hand
        self.gy = gy
        self.deck = deck
        self.field = field
        self.lp = lp
        self.can_summon = False

    def get_id(self):
        """Returns the Player's id."""
        return self.id

    def get_hand(self):
        """Returns the Player's hand."""
        return self.hand

    def get_gy(self):
        """Returns the Player's graveyard."""
        return self.gy

    def get_deck(self):
        """Returns the Player's deck."""
        return self.deck

    def get_field(self):
        """Returns the Player's field."""
        return self.field

    def get_lp(self):
        """Returns the Player's lifepoints."""
        return self.lp

    def set_hand(self, hand):
        """Sets the Player's hand."""
        self.hand = hand

    def set_gy(self, gy):
        """Sets the Player's graveyard."""
        self.gy = gy

    def set_deck(self, deck):
        """Sets the Player's deck."""
        self.deck = deck

    def set_field(self, field):
        """Sets the Player's field."""
        self.field = field

    def set_lp(self, lp):
        """Sets the Player's lifepoints."""
        self.lp = lp

    def change_lp(self, amount):
        """Adds the amount to the players lifepoints. Use a negative amount 
        value for subtraction.
        """
        self.lp += amount

    def can_draw(self):
        """Returns if a player is able to draw by checking if there are cards
        left in the Player's deck.
        """
        return len(self.deck) > 0

    def draw(self, number):
        """Adds number of card(s) from the Player's deck to their hand."""
        self.hand += self.deck.draw(number)

    def get_can_summon(self):
        """Returns if a Player is able to summon a monster by checking if
        there are monsters in their hand, if there are open spaces on their
        field, and if the Player has already summoned this turn.
        """
        monsters_in_hand = []
        for card in self.hand:
            if isinstance(card, Monster):
                monsters_in_hand.append(card)
        open_monster_zones = self.field.get_open_zones()
        return (self.can_summon and len(monsters_in_hand) and 
        		len(open_monster_zones))

    def set_can_summon(self, can_summon):
        """Sets the value for if the Player has summoned this turn to
        can_summon.
        """
        self.can_summon = can_summon

    def can_change_pos(self):
        """Returns if any monsters the Player controls is able to change
        their position.
        """
        monsters_can_change = []
        for monster in self.field.monster_zones:
            if monster:
                if monster.can_change_pos():
                    monsters_can_change.append(monster)
        return len(monsters_can_change) > 0

    def can_battle(self):
        """Returns if any monsters the Player controls is able to attack."""
        monsters_can_battle = []
        for monster in self.field.monster_zones:
            if monster:
                if monster.get_can_attack():
                    monsters_can_battle.append(monster)
        return len(monsters_can_battle) > 0