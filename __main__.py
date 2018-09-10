from card import *
from decklist import DeckList
from deck import Deck
from field import Field
from player import Player

def battle(monster1, monster2):
	pos1 = monster1.get_position()
	stats1 = monster1.get_stat()

	pos2 = monster2.get_position()
	stats2 = monster2.get_stat()

	diff = stats1 - stats2

	if pos2 == "ATTACK":
		return [True, diff]
	else:
		if diff > 0:
			return [True, 0]
		else:
			return [False, diff]

def try_int_input(prompt):
	result = -1
	try:
		result = int(input(prompt))
	except ValueError:
		pass
	return result

def main():
	bewd = Monster("Blue-Eyes White Dragon", "This legendary dragon is a powerful engine of destruction. Virtually invincible, very few have faced this awesome creature and lived to tell the tale.", 8, 3000, 2500)
	dm = Monster("Dark Magician","The ultimate wizard in terms of attack and defense.", 7, 2500, 2100)
	rebd = Monster("Red-Eyes Black Dragon", "", 7, 2400, 2000)
	bls = Monster("Black Luster Soldier", "", 8, 3000, 2500)
	ss = Monster("Summoned Skull", "", 6, 2500, 1200)
	dmg = Monster("Dark Magician Girl", "", 6, 2000, 1700)
	fgd = Monster("Five Headed Dragon", "", 12, 5000, 5000)
	cg = Monster("Celtic Guardian", "", 4, 1400, 1200)
	cod = Monster("Curse of Dragon", "", 5, 2000, 1500)
	gtfk = Monster("Gaia the Fierce Knight", "", 7, 2300, 2100)
	obelisk = Monster("Obelisk the Tormentor", "", 12, 4000, 4000)
	slifer = Monster("Slifer the Sky Dragon", "", 12, 4000, 4000)
	ra = Monster("The Winged Dragon of Ra", "", 12, 4000, 4000)
	kuriboh = Monster("Kuriboh", "", 1, 300, 200)

	cardlist = [bewd, dm, rebd, bls, ss, dmg, fgd, cg, cod, gtfk, obelisk, slifer, ra, kuriboh]

	deck_list1 = DeckList(1)
	for monster in cardlist:
		for i in range(3):
			deck_list1.add_card(monster)

	deck_list2 = DeckList(2)
	for monster in cardlist:
		for i in range(3):
			deck_list2.add_card(monster)

	#Set Up Game

	deck1 = Deck(deck_list1)
	deck2 = Deck(deck_list2)

	hand1 = []
	hand2 = []

	field1 = Field()
	field2 = Field()

	gy1 = []
	gy2 = []

	lp1 = 8000
	lp2 = 8000

	turn_count = 0
	phase = "DP"

	#Game Start
	deck1.shuffle()
	deck2.shuffle()

	player1 = Player(1, hand1, gy1, deck1, field1, lp1)
	player2 = Player(2, hand2, gy2, deck2, field2, lp2)
	players = [player1, player2]

	player1.draw(5)
	player2.draw(5)

	turn_player_idx = 0
	winner = None

	print("DUEL START")

	while player1.get_lp() > 0 and player2.get_lp() > 0 and winner == None:
		print("\n\n=====================================================")
		print("TURN: {}".format(turn_count + 1))
		turn_player = players[turn_player_idx]
		opposite_player_idx = abs(turn_player_idx - 1)
		opposite_player = players[abs(turn_player_idx - 1)]
		#Draw Phase
		phase = "DP"
		##Draw Card
		if turn_player.can_draw():
			print("Player {player_id_1} draws a card".format(player_id_1=turn_player.get_id()))
			turn_player.draw(1)
		else:
			print("Player {player_id_1} cannot draw.".format(player_id_1=turn_player.get_id(), player_id_2=opposite_player.get_id()))
			winner = opposite_player.get_id()
		for monster in turn_player.get_field().monster_zones:
			if monster != None:
				monster.unlock_attack()
				monster.unlock_position()
		turn_player.set_can_summon(True)

		#Main Phase
		phase = "MP"
		possible_moves = []
		if turn_player.get_can_summon():
			possible_moves.append("Summon")
			possible_moves.append("Set")
		if turn_player.can_change_pos():
			possible_moves.append("Change Battle Position")
		if turn_player.can_battle() and turn_count > 0:
			possible_moves.append("Go to Battle Phase")
		possible_moves.append("End Turn")
		while len(possible_moves) > 0:
			print("OPPONENT'S FIELD:")
			print("{} LP".format(opposite_player.get_lp()))
			print("HAND: {}".format(["x"] * len(opposite_player.get_hand())))
			print("DECK: {}".format(len(opposite_player.get_deck())))
			print(opposite_player.get_field().hidden())
			print("YOUR FIELD:")
			print("{} LP".format(turn_player.get_lp()))
			print("DECK: {}".format(len(turn_player.get_deck())))
			print(turn_player.get_field())
			print("HAND: {}".format(turn_player.get_hand()))
			print("You can do the following moves:")
			for i in range(len(possible_moves)):
				print("[{idx}] {action}".format(idx=i, action=possible_moves[i]))
			choice = try_int_input("What would you like to do: ")
			while choice >= len(possible_moves) or choice < 0:
				choice = try_int_input("Please enter a valid choice: ")

			#MAIN PHASE CHOICES
			if possible_moves[choice] == "Summon" or possible_moves[choice] == "Set":
				possible_monsters = []
				possible_monsters = turn_player.get_hand()
				for i in range(len(possible_monsters)):
					print("[{idx}] {monster} [{attack} ATK / {defense} DEF]".format(idx=i, monster=possible_monsters[i].get_name(), attack=possible_monsters[i].get_atk(), defense=possible_monsters[i].get_def()))
				monster_choice = try_int_input("Which card would you like to {}: ".format(possible_moves[choice]))
				while monster_choice >= len(possible_monsters) or monster_choice < 0:
					monster_choice = try_int_input("Please enter a valid choice: ")
				open_idx = turn_player.get_field().get_open_zones()[0]
				summon_monster = turn_player.get_hand().pop(monster_choice)
				if possible_moves[choice] == "Summon":
					turn_player.get_field().summon(summon_monster,open_idx)
					turn_player.set_can_summon(False)
					print("{monster} has been Summoned".format(monster=summon_monster.get_name()))
				if possible_moves[choice] == "Set":
					turn_player.get_field().set(summon_monster,open_idx)
					turn_player.set_can_summon(False)
					print("{monster} has been Set".format(monster=summon_monster.get_name()))
			elif possible_moves[choice] == "Change Battle Position":
				possible_monsters = []
				possible_monsters = turn_player.get_field().get_can_change_pos()
				monster_zones = turn_player.get_field().monster_zones
				for i in range(len(possible_monsters)):
					print("[{idx}] {monster} [{attack} ATK / {defense} DEF]".format(idx=i, monster=monster_zones[possible_monsters[i]].get_name(), attack=monster_zones[possible_monsters[i]].get_atk(), defense=monster_zones[possible_monsters[i]].get_def()))
				monster_choice = try_int_input("Which card would you like to change position: ")
				while monster_choice >= len(possible_monsters) or monster_choice < 0:
					monster_choice = try_int_input("Please enter a valid choice: ")
				pos_change_monster = monster_zones[possible_monsters[monster_choice]]
				pos_change_monster.change_pos()
			elif possible_moves[choice] == "Go to Battle Phase":
				phase = "BP"
			
			#BATTLE PHASE CHOICES
			elif possible_moves[choice] == "Attack":
				possible_monsters = []
				possible_monsters = turn_player.get_field().get_can_attack()
				monster_zones = turn_player.get_field().monster_zones
				for i in range(len(possible_monsters)):
					print("[{idx}] {monster} {stat} {pos}".format(idx=i, monster=monster_zones[possible_monsters[i]].get_name(), stat=monster_zones[possible_monsters[i]].get_stat(), pos=monster_zones[possible_monsters[i]].get_position()))
				monster_choice = try_int_input("Which card would you like to attack with: ")
				while monster_choice >= len(possible_monsters) or monster_choice <0:
					monster_choice = try_int_input("Please enter a valid choice: ")
				attacker = monster_zones[possible_monsters[monster_choice]]
				attacker_idx = possible_monsters[monster_choice]
				possible_targets = []
				possible_targets = opposite_player.get_field().get_monsters()
				opp_monster_zones = opposite_player.get_field().monster_zones
				if len(possible_targets) > 0:
					for i in range(len(possible_targets)):
						print("[{idx}] {monster} {stat} {pos}".format(idx=i, monster= "???" if opp_monster_zones[possible_targets[i]].get_is_set() else opp_monster_zones[possible_targets[i]].get_name(), stat= "SET" if opp_monster_zones[possible_targets[i]].get_is_set() else opp_monster_zones[possible_targets[i]].get_stat(), pos=opp_monster_zones[possible_targets[i]].get_position()))
					target_choice = try_int_input("Which card would you like to attack: ")
					while target_choice >= len(possible_targets) or target_choice <0:
						target_choice = try_int_input("Please enter a valid choice: ")
					target = opp_monster_zones[possible_targets[target_choice]]
					target_idx = possible_targets[target_choice]
					battle_result = battle(attacker, target)
					print("{attacker} [{attacker_stat} ATTACK] ATTACKS {target} [{target_stat} {target_pos}]".format(attacker=attacker.get_name(), attacker_stat=attacker.get_atk(), target=target.get_name(), target_stat=target.get_stat(), target_pos=target.get_position()))
					##ATTACK WIN
					if battle_result[0] and battle_result[1] > 0:
						print("{attacker} WINS. {target} DESTROYED".format(attacker=attacker.get_name(), target=target.get_name()))
						opposite_player.get_gy().append(opposite_player.get_field().remove(attacker_idx))
						opposite_player.change_lp(-1 * battle_result[1])
						attacker.lock_attack()
			
					##ATTACK LOSE
					elif battle_result[0] and battle_result[1] < 0:
						print("{target} WINS. {attacker} DESTROYED".format(attacker=attacker.get_name(), target=target.get_name()))
						turn_player.get_gy().append(turn_player.get_field().remove(target_idx))
						turn_player.change_lp(battle_result[1])
			
					##ATTACK TIE
					elif battle_result[0] and battle_result[1] == 0:
						print("BATTLE TIE. {attacker} and {target} DESTROYED".format(attacker=attacker.get_name(), target=target.get_name()))
						turn_player.get_gy().append(turn_player.get_field().remove(attacker_idx))
						opposite_player.get_gy().append(opposite_player.get_field().remove(target_idx))
			
					##DEF LOSE
					elif not battle_result[0] and battle_result[1] < 0:
						print("{attacker} LOSES. {target} NOT DESTROYED".format(attacker=attacker.get_name(), target=target.get_name()))
						turn_player.change_lp(battle_result[1])
						attacker.lock_attack()
						if target.get_is_set():
							target.flip()
					##DEF WIN
					elif not battle_result[0] and battle_result[1] > 0:
						print("{attacker} WINS. {target} DESTROYED".format(attacker=attacker.get_name(), target=target.get_name()))
						opposite_player.get_gy().append(opposite_player.get_field().remove(target_idx))
						attacker.lock_attack()
					##DEF TIE
					else:
						print("NO MONSTERS DESTROYED")
						if target.get_is_set():
							target.flip()
						attacker.lock_attack()
				else:
					print("{attacker} attacks Player {player} directly".format(attacker=attacker.get_name(), player=opposite_player.get_id()))
					damage = -1 * attacker.get_atk()
					opposite_player.change_lp(damage)
					attacker.lock_attack()
				if turn_player.get_lp() <= 0:
					turn_player.set_lp(0)
					winner = opposite_player.get_id()
					break
				elif opposite_player.get_lp() <= 0:
					opposite_player.set_lp(0)
					winner = turn_player.get_id()
					break

			elif possible_moves[choice] == "End Turn":
				phase = "EP"

			possible_moves = []
			if phase == "MP":
				if turn_player.get_can_summon():
					possible_moves.append("Summon")
					possible_moves.append("Set")
				if turn_player.can_change_pos():
					possible_moves.append("Change Battle Position")
				if turn_player.can_battle() and turn_count > 0:
					possible_moves.append("Go to Battle Phase")
				possible_moves.append("End Turn")
			elif phase == "BP":
				if turn_player.can_battle():
					possible_moves.append("Attack")
				possible_moves.append("End Turn")
			elif phase =="EP":
				#End Phase
				#Check hand count > 6
				while len(turn_player.get_hand()) > 6:
					current_hand = turn_player.get_hand()
					for i in range(len(current_hand)):
						print("[{idx}] {card} [{attack} ATK / {defense} DEF]".format(idx=i, card=current_hand[i].get_name(), attack=current_hand[i].get_atk(), defense=current_hand[i].get_def()))
					choice = try_int_input("Too many cards in your hand. You have {}, you can only have up to 6. Which card will you discard: ".format(len(current_hand)))
					while choice > len(current_hand) or choice < 0:
						choice = input("Please enter a valid choice: ")
					current_hand.pop(choice)
				##Increment turn count
				turn_count += 1
				## Change Player
				turn_player_idx = opposite_player_idx
			else:
				print("You shouldn't be here.")
	
	print("PLAYER {} WINS!".format(winner))

if __name__ == '__main__':
	main()
