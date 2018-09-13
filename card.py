class Card:

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.is_set = False

    def __repr__(self):
        return self.name

    def full_string(self):
        return "{name}\n{desc}".format(name=self.name, desc=self.desc)

    def get_name(self):
        return self.name

    def get_desc(self):
        return self.desc

    def get_is_set(self):
        return self.is_set


class Monster(Card):

    def __init__(self, name, desc, level, attack, defense):
        super().__init__(name, desc)
        self.level = level
        self.attack = attack
        self.defense = defense
        self.position = None
        self.turn_count = 0
        self.can_change_position = False
        self.can_attack = False

    def full_string(self):
        return "{name}\n{level}\nMONSTER\n{desc}\n[ATK:{attack}/DEF:{defense}]"\
        		.format(name=self.name, level="*" * self.level, desc=self.desc, 
        			    attack=self.attack, defense=self.defense)

    def get_level(self):
        return self.level

    def get_atk(self):
        return self.attack

    def get_def(self):
        return self.defense

    def get_position(self):
        return self.position

    def summon(self, is_set, position):
        self.is_set = is_set
        if is_set:
            self.position = "DEFENSE"
        else:
            self.position = position.upper()
            self.can_attack = True

    def remove(self):
        self.position = None
        self.is_set = False
        self.can_attack = False
        self.can_change_position = None

    def get_stat(self):
        if self.position.upper() == "DEFENSE":
            return self.get_def()
        elif self.position.upper() == "ATTACK":
            return self.get_atk()
        else:
            return None

    def get_can_attack(self):
        return self.can_attack and self.position == "ATTACK"

    def can_change_pos(self):
        return self.can_change_position

    def flip(self):
        if self.is_set:
            self.is_set = False

    def change_pos(self):
        if self.position == "DEFENSE":
            self.position = "ATTACK"
        elif self.position == "ATTACK":
            self.position = "DEFENSE"
        self.flip()
        self.can_change_position = False

    def lock_attack(self):
        self.can_attack = False

    def unlock_attack(self):
        self.can_attack = True

    def lock_position(self):
        self.can_change_position = False

    def unlock_position(self):
        self.can_change_position = True


class Spell(Card):
    def __repr__(self):
        return "{name}\nSPELL\n{desc}".format(name=self.name, desc=self.desc)


class Trap(Card):
    def __repr__(self):
        return "{name}\nTRAP\n{desc}".format(name=self.name, desc=self.desc)