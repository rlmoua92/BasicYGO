#from card_zone import *


class Field:

    def __init__(self):
        self.monster_zones = [None for i in range(5)]
        #self.st_zones = [SpellTrapCardZone() for i in range(5)]

    def __repr__(self):
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
        open_zones = []
        for i in range(len(self.monster_zones)):
            if not self.monster_zones[i]:
                open_zones.append(i)
        return open_zones

    def get_monsters(self):
        monsters = []
        for i in range(len(self.monster_zones)):
            if self.monster_zones[i]:
                monsters.append(i)
        return monsters

    def get_can_attack(self):
        can_attack_list = []
        for i in range(len(self.monster_zones)):
            if self.monster_zones[i]:
                if self.monster_zones[i].get_can_attack():
                    can_attack_list.append(i)
        return can_attack_list

    def get_can_change_pos(self):
        can_change_pos_list = []
        for i in range(len(self.monster_zones)):
            if self.monster_zones[i]:
                if self.monster_zones[i].can_change_pos():
                    can_change_pos_list.append(i)
        return can_change_pos_list

    def get_zone(self, idx):
        return self.monster_zones[idx]

    def summon(self, card, idx):
        if idx not in self.get_open_zones():
            print("Cannot Summon. Zone already taken.")
            return False
        else:
            card.summon(False, "ATTACK")
            self.monster_zones[idx] = card
            return True

    def set(self, card, idx):
        if idx not in self.get_open_zones():
            print("Cannot Set. Zone already taken.")
            return False
        else:
            card.summon(True, "DEFENSE")
            self.monster_zones[idx] = card
            return True

    def remove(self, idx):
        if idx in self.get_open_zones():
            print("Cannot Remove. Zone is empty.")
            return None
        else:
            card = self.monster_zones[idx]
            card.remove()
            self.monster_zones[idx] = None
            return card