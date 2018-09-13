from card import Card, Monster

class Player:
    def __init__(self, id, hand, gy, deck, field, lp=8000):
        self.id = id
        self.hand = hand
        self.gy = gy
        self.deck = deck
        self.field = field
        self.lp = lp
        self.can_summon = False

    def get_id(self):
        return self.id

    def get_hand(self):
        return self.hand

    def get_gy(self):
        return self.gy

    def get_deck(self):
        return self.deck

    def get_field(self):
        return self.field

    def get_lp(self):
        return self.lp

    def set_hand(self, hand):
        self.hand = hand

    def set_gy(self, gy):
        self.gy = gy

    def set_deck(self, deck):
        self.deck = deck

    def set_field(self, field):
        self.field = field

    def set_lp(self, lp):
        self.lp = lp

    def change_lp(self, amount):
        self.lp += amount

    def can_draw(self):
        return len(self.deck) > 0

    def draw(self, number):
        self.hand += self.deck.draw(number)

    def get_can_summon(self):
        monsters_in_hand = []
        for card in self.hand:
            if type(card) == Monster:
                monsters_in_hand.append(card)
        open_monster_zones = self.field.get_open_zones()
        return self.can_summon and len(monsters_in_hand) > 0 and len(open_monster_zones) > 0

    def set_can_summon(self, can_summon):
        self.can_summon = can_summon

    def can_change_pos(self):
        monsters_can_change = []
        for monster in self.field.monster_zones:
            if monster != None:
                if monster.can_change_pos():
                    monsters_can_change.append(monster)
        return len(monsters_can_change) > 0

    def can_battle(self):
        monsters_can_battle = []
        for monster in self.field.monster_zones:
            if monster != None:
                if monster.get_can_attack():
                    monsters_can_battle.append(monster)
        return len(monsters_can_battle) > 0
