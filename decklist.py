"""
This module contains the Field class used to represent a decklist.
"""

from card import Card, Monster


class DeckList:

    """
    This is a class to represent a decklist.

    Attributes:
        decklist (dictionary): The keys are the name of the cards. The values
        are a list containing the Card at index 0 and the card count at 
        index 1.
        deck_count (int): The total number of cards in the decklist.
        min_limit (int): The minimum number of cards for a valid decklist.
        max_limit (int): The maximum number of cards for a valid decklist.
    """
    
    def __init__(self, decklist=None, min=40, max=60):
        """The constructor for the DeckList class.

        Parameters:
            decklist (dictionary): The keys are the name of the cards. The values
            are a list containing the Card at index 0 and the card count at 
            index 1. Defaults to None and is then assigned an empty dictionary.
            min (int): The minimum number of cards for a valid decklist.
            Defaults to 40.
            max (int): The maximum number of cards for a valid decklist.
            Defaults to 60.
        """
        if not decklist:
            self.decklist = {}
        else:
            self.decklist = decklist
        self.deck_count = sum(value[1] for value in self.decklist.values())
        self.min_limit = min
        self.max_limit = max

    def __repr__(self):
        """The string representation for the DeckList class.

        Returns:
            A string with each Card and count in the DeckList and the total 
            card count.
        """
        result = ""
        for key in self.decklist.keys():
            result += "{name}: {count}\n".format(
            	name=key, 
            	count=self.decklist[key][1]
            )
        result += "Total Cards: {total_count}".format(
        	total_count=self.deck_count
        )
        return result

    def is_valid(self):
        """Returns if the DeckList is valid by checking if the total card
        count is at least the minimum and less than the maximum, and if any
        card has more than 3 copies.
        """
        if self.deck_count < self.min_limit:
            print(
            	"NOT ENOUGH CARDS IN DECK\nDeck contains {count} cards. "
            	"Must contain at least {min_limit} cards.".format(
            		count=deck_count, 
            		min_limit=self.min_limit
            	)
            )
            return False
        if self.deck_count > self.max_limit:
            print(
            	"TOO MANY CARDS IN DECK\nDeck contains {count} cards. "
            	"Can only contain at most {max_limit} cards.".format(
            		count=deck_count, 
            		max_limit=self.max_limit
            	)
            )
        too_many_copies = False
        for key in self.decklist.keys():
            if self.decklist[key][1] > 3:
                if not too_many_copies:
                    too_many_copies = True
                    print(
                    	"TOO MANY COPIES\nDeck can only contain 3 copies "
                    	"of a single card. There are too many copies of the "
                    	"following cards:"
                    )
                print("{name}: {count}".format(
                	name=key, 
                	count=self.decklist[key][1]
                ))
        if too_many_copies:
            return False
        return True
                
    def add_card(self, card):
        """Adds 1 copy of Card card to the DeckList.

        Returns True if the card was added correctly.
        Returns False if the card could not be added because there are already
        3 copies or because the DeckList is already at the maximum count.
        """
        current_count = self.decklist.get(card.get_name(), [0,0])[1]
        if current_count < 3 and self.deck_count < self.max_limit:
            current_count += 1
            self.decklist[card.get_name()] = [card, current_count]
            self.deck_count += 1
            print(
            	"{name} added to the Deck. Now there are {copy_count} "
            	"copies in the Deck".format(
            		name=card.get_name(), 
            		copy_count=current_count
            	)
            )
            return True
        else:
            print(
            	"Could not add {name} to Deck.".format(name=card.get_name())
            )
            if current_count >= 3:
                print("There are already 3 copies in the Deck.")
            elif self.deck_count < self.max_limit:
                print(
                	"There are already {max_limit} cards in the Deck.".format(
                		max_limit=self.max_limit
                	)
                )
            return False

    def remove_card(self, card):
        """Removes 1 copy of Card card from the DeckList.

        Returns True if the card was removed correctly.
        Returns False if the card could not be removed because there are no
        copies or because the DeckList has no cards.
        """
        current_count = self.decklist.get(card.get_name(), [0,0])[1]
        if current_count > 0 and self.deck_count > 0:
            current_count -= 1
            if current_count == 0:
                pass
            else:
                self.decklist[card.get_name()] = [card, current_count]
            self.deck_count -= 1
            print(
            	"{name} removed from the Deck. Now there are {copy_count} "
            	"copies in the Deck".format(
            		name=card.get_name(), 
            		copy_count=current_count
            	)
            )
            return True
        else:
            print("Could not remove {name} from Deck.".format(
            	name=card.get_name()
            ))
            if current_count == 0:
                print("There are already no copies in the Deck.")
            elif self.deck_count == 0:
                print("There are no cards in the Deck. ")
            return False

    def to_list(self):
        """Returns a list representation of the decklist dict."""
        result = []
        for key in self.decklist.keys():
            for i in range(self.decklist[key][1]):
                monster = self.decklist[key][0]
                result.append(Monster(monster.get_name(), monster.get_desc(), 
                					  monster.get_level(), monster.get_atk(), 
                					  monster.get_def()
                ))
        return result