"""
This module contains the Card class used to represent a card.
It also contains the Card subclasses: Monster, Spell, and Trap.
"""

class Card:

    """
    This is a class to represent a card.

    Attributes:
        name (str): The name of the card.
        desc (str): The description of the card.
        is_set (bool): Whether the card is Face-down or not.
    """
    
    def __init__(self, name, desc):
        """The constructor for the Card class
        
        Attributes:
            name (str): The name of the card.
            desc (str): The description of the card.
        """
        self.name = name
        self.desc = desc
        self.is_set = False

    def __repr__(self):
        """The string representation for the Card class.

        Returns:
            A string with the Card name.
        """
        return self.name

    def full_string(self):
        """The full string representation for the Card class.

        Returns:
            A string with the Card name and Card description.
        """
        return "{name}\n{desc}".format(name=self.name, desc=self.desc)

    def get_name(self):
        """Returns the name of the Card."""
        return self.name

    def get_desc(self):
        """Returns the description of the Card."""
        return self.desc

    def get_is_set(self):
        """Returns if the Card is Face-down or not."""
        return self.is_set


class Monster(Card):

    """
    This is a class to represent a monster card.

    Attributes:
        name (str): The name of the card.
        desc (str): The description of the card.
        is_set (bool): Whether the card is Face-down or not.
        level (int): The level of the monster.
        attack (int): The attack of the monster.
        defense (int): The defense of the monster.
        position (str): The position of the monster.
        turn_count (int): How many turns the monster has been on the field.
        can_change_position (bool): If the monster can change positions.
        can_attack (bool): If the monster can attack.
    """
    
    def __init__(self, name, desc, level, attack, defense):
        """The constructor for the Monster class.

        Parameters:
            name (str): The name of the card.
            desc (str): The description of the card.
            level (int): The level of the monster.
            attack (int): The attack of the monster.
            defense (int): The defense of the monster.
        """
        super().__init__(name, desc)
        self.level = level
        self.attack = attack
        self.defense = defense
        self.position = None
        self.turn_count = 0
        self.can_change_position = False
        self.can_attack = False

    def full_string(self):
        """The full string representation for the Monster class.

        Returns:
            A string with the Card name, Monster level, an indication of the 
            Monster class, Card description, Monster attack points, Monster 
            defense points.
        """
        return "{name}\n{level}\nMONSTER\n{desc}\n[ATK:{attack}/DEF:{defense}]"\
        		.format(name=self.name, level="*" * self.level, desc=self.desc, 
        			    attack=self.attack, defense=self.defense)

    def get_level(self):
        """Returns the level of the Monster."""
        return self.level

    def get_atk(self):
        """Returns the attack of the Monster."""
        return self.attack

    def get_def(self):
        """Returns the defense of the Monster."""
        return self.defense

    def get_position(self):
        """Returns the position of the Monster."""
        return self.position

    def summon(self, is_set, position):
        """Values are set for the scenario when the Monster is summmoned to 
        the field. is_set sets if the Monster will be Face-down and position
        sets the position of the Monster.
        """
        self.is_set = is_set
        if is_set:
            self.position = "DEFENSE"
        else:
            self.position = position.upper()
            self.can_attack = True

    def remove(self):
        """Resets values for scenario when the Monster is removed from the 
        field.
        """
        self.position = None
        self.is_set = False
        self.can_attack = False
        self.can_change_position = None

    def get_stat(self):
        """Returns the attack or defense of the Monster depending on
        which position it is in.
        """
        if self.position.upper() == "DEFENSE":
            return self.get_def()
        elif self.position.upper() == "ATTACK":
            return self.get_atk()
        else:
            return None

    def get_can_attack(self):
        """Returns if the Monster can attack."""
        return self.can_attack and self.position == "ATTACK"

    def can_change_pos(self):
        """Returns if the Monster can change position."""
        return self.can_change_position

    def flip(self):
        """If the Monster is Face-down it is changed to Face-Up."""
        if self.is_set:
            self.is_set = False

    def change_pos(self):
        """Changes the position of a Monster from defense to attack and
        vice versa. If the Monster is Face-down it is also changed to 
        Face-Up.
        """
        if self.position == "DEFENSE":
            self.position = "ATTACK"
        elif self.position == "ATTACK":
            self.position = "DEFENSE"
        self.flip()
        self.can_change_position = False

    def lock_attack(self):
        """Makes it so the Monster cannot attack."""
        self.can_attack = False

    def unlock_attack(self):
        """Makes it so the Monster can attack."""
        self.can_attack = True

    def lock_position(self):
        """Makes it so the Monster cannot change position."""
        self.can_change_position = False

    def unlock_position(self):
        """Makes it so the Monster can change position."""
        self.can_change_position = True


class Spell(Card):

    """
    This is a class to represent a Spell Card.

    Attributes:
        name (str): The name of the card.
        desc (str): The description of the card.
        is_set (bool): Whether the card is Face-down or not.
    """
    
    def __repr__(self):
        """The string representation for the Spell class.

        Returns:
            A string with the Card name, an indication of the Spell class, and
            Card description.
        """
        return "{name}\nSPELL\n{desc}".format(name=self.name, desc=self.desc)


class Trap(Card):
 
    """
    This is a class to represent a Trap Card.

    Attributes:
        name (str): The name of the card.
        desc (str): The description of the card.
        is_set (bool): Whether the card is Face-down or not.
    """
    
    def __repr__(self):
        """The string representation for the Trap class.

        Returns:
            A string with the Card name, an indication of the Trap class, and
            Card description.
        """
        return "{name}\nTRAP\n{desc}".format(name=self.name, desc=self.desc)