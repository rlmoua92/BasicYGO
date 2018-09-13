"""
This module contains the Field class used to represent a player's field in a 
Duel.
"""

#from card_zone import *


class Field:

    """
    This is a class to represent a player's field in a Duel.

    Attributes:
        monster_zones (list): The zones a monster can exist on.
    """

    def __init__(self):
        """The constructor for the Field class. Monster zones are initialized
        as a list of 5 None values.
        """
        self.monster_zones = [None for i in range(5)]
        #self.st_zones = [SpellTrapCardZone() for i in range(5)]

    def __repr__(self):
        """The string representation for the Field class.

        Returns:
            A string that visually represents the current field. Zones with
            monsters display the monster's information. Zones without monsters
            display an X. Each zone is separated by a |.
            """
        result = ""
        result += "| "
        for card in self.monster_zones:
            if not card:
                result += "X"
            elif card.get_is_set():
                result += "(SET) {name}: {stats} {position}".format(
                	name=card.get_name(), 
                	stats=card.get_stat(), 
                	position=card.get_position()
                )
            else:
                result += "{name}: {stats} {position}".format(
                	name=card.get_name(), 
                	stats=card.get_stat(), 
                	position=card.get_position()
                )
            result += " | "
        #result += "\n| "
        #for zone in self.st_zones:
        #    if zone.card == None:
        #        result += "X"
        #    elif zone.is_set():
        #        result += "SET CARD"
        #    else:
        #        result += zone.card.name
        #    result += " |"
        return result

    def hidden(self):
        """Returns a string that visually represents the hidden version of the
        current field. Information that is not available to all players is
        hidden.

        This is used so that an opposing player may not have information that
        another player may not want them to have.

        Example: The opponent should not have knowledge about a Face-Down card.
        """
        result = ""
        result +="| "
        for card in self.monster_zones:
            if not card:
                result += "X"
            elif card.get_is_set():
                result += "SET CARD: {position}".format(
                	position=card.get_position()
                )
            else:
                result += "{name}: {stats} {position}".format(
                	name=card.get_name(), 
                	stats=card.get_stat(), 
                	position=card.get_position()
                )
            result += " | "
        #result += "\n| "
        #for zone in self.st_zones:
        #    if zone.card == None:
        #        result += "X"
        #    elif zone.is_set():
        #        result += "SET CARD"
        #    else:
        #        result += zone.card.name
        #    result += " |"
        return result

    def get_open_zones(self):
        """Returns a list containing the indexes of monster_zones that
        do not contain a monster.
        """
        open_zones = []
        for i in range(len(self.monster_zones)):
            if not self.monster_zones[i]:
                open_zones.append(i)
        return open_zones

    def get_monsters(self):
        """Returns a list containing the indexes of monster_zones that
        contain a monster.
        """
        monsters = []
        for i in range(len(self.monster_zones)):
            if self.monster_zones[i]:
                monsters.append(i)
        return monsters

    def get_can_attack(self):
        """Returns a list containing the indexes of monster_zones that
        contain a monster that can attack.
        """
        can_attack_list = []
        for i in range(len(self.monster_zones)):
            if self.monster_zones[i]:
                if self.monster_zones[i].get_can_attack():
                    can_attack_list.append(i)
        return can_attack_list

    def get_can_change_pos(self):
        """Returns a list containing the indexes of monster_zones that
        contain a monster that can change its position.
        """
        can_change_pos_list = []
        for i in range(len(self.monster_zones)):
            if self.monster_zones[i]:
                if self.monster_zones[i].can_change_pos():
                    can_change_pos_list.append(i)
        return can_change_pos_list

    def get_zone(self, idx):
        """Returns the value of monster_zones at the index idx.
        Returns None if there is no monster.
        Returns a Monster instance if there is a monster.
        """
        return self.monster_zones[idx]

    def summon(self, card, idx):
        """Sets the value of monster_zones at the index idx to the Monster
        instance provided by card in Face-up attack position.

        Returns False if the monster wasn't summoned because the zone was
        already taken.
        Returns True if the monster was summoned correctly.
        """
        if idx not in self.get_open_zones():
            print("Cannot Summon. Zone already taken.")
            return False
        else:
            card.summon(False, "ATTACK")
            self.monster_zones[idx] = card
            return True

    def set(self, card, idx):
        """Sets the value of monster_zones at the index idx to the Monster
        instance provided by card in Face-down defense position.

        Returns False if the monster wasn't set because the zone was
        already taken.
        Returns True if the monster was set correctly.
        """
        if idx not in self.get_open_zones():
            print("Cannot Set. Zone already taken.")
            return False
        else:
            card.summon(True, "DEFENSE")
            self.monster_zones[idx] = card
            return True

    def remove(self, idx):
        """Removes the monster at index idx of monster_zones.

        Returns None if the Zone is empty.
        Returns the instance of the Monster if it was removed correctly."""
        if idx in self.get_open_zones():
            print("Cannot Remove. Zone is empty.")
            return None
        else:
            card = self.monster_zones[idx]
            card.remove()
            self.monster_zones[idx] = None
            return card