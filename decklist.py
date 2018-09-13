from card import Card, Monster


class DeckList:

    def __init__(self, id, decklist=None, min=40, max=60):
        if type(decklist) != dict:
            print("Invalid type! Decklist must be a dict. Try again.")
            self.decklist = {}
        else:
            self.decklist = decklist
        self.id = id
        self.deck_count = sum(value[1] for value in self.decklist.values())
        self.min_limit = min
        self.max_limit = max

    def __repr__(self):
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

    def remove_card(self, card):
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
        else:
            print("Could not remove {name} from Deck.".format(
            	name=card.get_name()
            ))
            if current_count == 0:
                print("There are already no copies in the Deck.")
            elif self.deck_count == 0:
                print("There are no cards in the Deck. ")

    def to_list(self):
        result = []
        for key in self.decklist.keys():
            for i in range(self.decklist[key][1]):
                monster = self.decklist[key][0]
                result.append(Monster(monster.get_name(), monster.get_desc(), 
                					  monster.get_level(), monster.get_atk(), 
                					  monster.get_def()
                ))
        return result