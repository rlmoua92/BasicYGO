"""class CardZone:
	def __init__(self):
		self.card = None
		self.set = False
		self.turn_count = 0
		self.position_lock = True
		self.attack_lock = False

	def get_card(self):
		return self.card

	def is_set(self):
		return self.set

	def play_card(self, card, is_set):
		self.card = card
		self.set = is_set

	def remove_card(self):
		old_card = self.card
		self.card = None
		self.set = False
		self.turn_count = 0
		return old_card

	def inc_turn_count(self):
		self.turn_count += 1

	def get_turn_count(self):
		return self.turn_count

	def unlock_position(self):
		self.position_lock = False

	def unlock_attack(self):
		self.attack_lock = False

	def lock_attack(self):
		self.attack_lock = True

class MonsterCardZone(CardZone):
	def __init__(self):
		super().__init__()
		self.position = None

	def get_monster_position(self):
		return self.position

	def get_stat(self):
		if self.get_monster_position() == "ATTACK":
			return self.get_card().get_atk()
		else:
			return self.get_card().get_def()

	def play_card(self, card, is_set, position):
		super().play_card(card, is_set)
		if is_set:
			self.position.upper() = "DEFENSE"
		else:
			self.position = position.upper()

	def remove_card(self):
		self.position = None
		return super().remove_card()

	def change_position(self, new_position):
		if self.position_lock:
			print("Can't change position of card.")
		else:
			old_position = self.position.upper()
			self.position = new_position.upper()
			old_set = self.set
			if old_set == True and old_position.upper() == "DEFENSE" and new_position.upper() == "ATTACK":
				self.set = False
			self.position_lock = True
			print("Card changed from {old_set} {old_position} position to {new_set} {new_position} position".format(old_set="FACE-UP" if old_set else "FACE-DOWN", new_set="FACE-UP" if self.set else "FACE-DOWN", old_position=old_position, new_position=self.position))


class SpellTrapCardZone(CardZone):
	def __init__(self):
		super().__init__()"""