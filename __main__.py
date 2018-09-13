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
    bewd = Monster("Blue-Eyes White Dragon", "This legendary dragon is a "
        "powerful engine of destruction. Virtually invincible, very few have "
        "faced this awesome creature and lived to tell the tale.", 8, 3000, 
        2500)
    dm = Monster("Dark Magician","The ultimate wizard in terms of attack and "
        "defense.", 7, 2500, 2100)
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
    cardlist = [
        bewd, dm, rebd, bls, ss, dmg, fgd, cg, cod, gtfk, obelisk, slifer, 
        ra, kuriboh
    ]
    deck_list1 = DeckList(1)
    for monster in cardlist:
        for i in range(3):
            deck_list1.add_card(monster)
    deck_list2 = DeckList(2)
    for monster in cardlist:
        for i in range(3):
            deck_list2.add_card(monster)

    # These variables initialize the classes need to set up the Duel.
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
    turn_player_idx = 0
    player1 = Player(1, hand1, gy1, deck1, field1, lp1)
    player2 = Player(2, hand2, gy2, deck2, field2, lp2)
    players = [player1, player2]
    winner = None

    # These functions start the Duel using the variables defined above.
    # Both decks are shuffled and both players draw 5 cards.
    deck1.shuffle()
    deck2.shuffle()
    player1.draw(5)
    player2.draw(5)
    print("DUEL START")

    # This while loop contols the actions that the players can take in the
    # Duel. It will not close until the Duel is over (i.e. a Player's 
    # LifePoints hit 0, a Player can't draw any more cards, etc...)
    while player1.get_lp() > 0 and player2.get_lp() > 0 and not winner:
        # This section prints out the visualtion of the current state of
        # of the Duel (i.e. Turn Count, Each Player's Hand, Field, LP, etc...)
        print("\n\n=====================================================")
        print("TURN: {}".format(turn_count + 1))
        turn_player = players[turn_player_idx]
        opposite_player_idx = abs(turn_player_idx - 1)
        opposite_player = players[abs(turn_player_idx - 1)]

        # This section handles the logic of the Draw Phase.
        # If the player can draw a card, they draw it. If not the game is over
        # and the opponent wins. Also, in this phase all action locks are 
        # reset. (i.e. Monsters not being able to Attack or change their
        # Positions)
        phase = "DP"
        if turn_player.can_draw():
            print("Player {player_id_1} draws a card".format(
                  player_id_1=turn_player.get_id()
            ))
            turn_player.draw(1)
        else:
            print("Player {player_id_1} cannot draw.".format(
                  player_id_1=turn_player.get_id(), 
                  player_id_2=opposite_player.get_id()
            ))
            winner = opposite_player.get_id()
        for monster in turn_player.get_field().monster_zones:
            if monster != None:
                monster.unlock_attack()
                monster.unlock_position()
        turn_player.set_can_summon(True)

        # This section adds the intial actions the Player can take during
        # the Main Phase. After choosing from the selections the user enters
        # the actions while loop and choose from those choices until their
        # turn is over.
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

        # This loop tells the Player what actions they can currently take.
        # It uses an input prompt so the Player can select an action.
        while possible_moves:
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
                print("[{idx}] {action}".format(
                      idx=i, 
                      action=possible_moves[i])
                )
            choice = try_int_input("What would you like to do: ")
            while choice >= len(possible_moves) or choice < 0:
                choice = try_int_input("Please enter a valid choice: ")

            # This section handles the logic for actions the Player can take
            # during their Main Phase.
            # Summon: If able, summon a monster from your hand in Face-up
            # Attack Position.
            # Set: If able, set a monster from your hand in Face-down Defense
            # Position.
            # Change Battle Position: If able, change the Position of a
            # monster you control. (i.e. Attack to Defense, Face-down Defense
            # to Face-up Attack, etc...)
            # Go to Battle Phase: Go to Battle Phase.
            if (possible_moves[choice] == "Summon" or 
                possible_moves[choice] == "Set"):
                possible_monsters = []
                possible_monsters = turn_player.get_hand()
                for i in range(len(possible_monsters)):
                    print(
                        "[{idx}] {monster} "
                        "[{attack} ATK / {defense} DEF]".format(
                            idx=i, monster=possible_monsters[i].get_name(), 
                            attack=possible_monsters[i].get_atk(), 
                            defense=possible_monsters[i].get_def()
                        )
                    )
                monster_choice = try_int_input(
                    "Which card would you like to {}: ".format(
                        possible_moves[choice]
                    )
                )
                while (monster_choice >= len(possible_monsters) or 
                       monster_choice < 0):
                    monster_choice = try_int_input(
                        "Please enter a valid choice: "
                    )
                open_idx = turn_player.get_field().get_open_zones()[0]
                summon_monster = turn_player.get_hand().pop(monster_choice)
                if possible_moves[choice] == "Summon":
                    turn_player.get_field().summon(summon_monster,open_idx)
                    turn_player.set_can_summon(False)
                    print("{monster} has been Summoned".format(
                          monster=summon_monster.get_name()
                    ))
                if possible_moves[choice] == "Set":
                    turn_player.get_field().set(summon_monster,open_idx)
                    turn_player.set_can_summon(False)
                    print("{monster} has been Set".format(
                          monster=summon_monster.get_name()
                    ))
            elif possible_moves[choice] == "Change Battle Position":
                possible_monsters = []
                possible_monsters = turn_player.get_field()\
                                    .get_can_change_pos()
                monster_zones = turn_player.get_field().monster_zones
                for i in range(len(possible_monsters)):
                    print("[{idx}] {monster} [{attack} ATK / {defense} DEF]"\
                          .format(
                              idx=i, 
                              monster=monster_zones[possible_monsters[i]]\
                                      .get_name(), 
                              attack=monster_zones[possible_monsters[i]]\
                                      .get_atk(), 
                              defense=monster_zones[possible_monsters[i]]\
                                      .get_def()))
                monster_choice = try_int_input(
                    "Which card would you like to change position: "
                )
                while (monster_choice >= len(possible_monsters) or 
                       monster_choice < 0):
                    monster_choice = try_int_input(
                        "Please enter a valid choice: "
                    )
                pos_change_monster = \
                    monster_zones[possible_monsters[monster_choice]]
                pos_change_monster.change_pos()
            elif possible_moves[choice] == "Go to Battle Phase":
                phase = "BP"
            
            # This section handles the logic for actions the Player can take
            # during their Battle Phase.
            # Attack: If able, the Player's monster can either attack the
            # opponent's monster or the opponent directly if they have no
            # monsters.
            elif possible_moves[choice] == "Attack":
                possible_monsters = []
                possible_monsters = turn_player.get_field().get_can_attack()
                monster_zones = turn_player.get_field().monster_zones
                for i in range(len(possible_monsters)):
                    print("[{idx}] {monster} {stat} {pos}".format(
                        idx=i, 
                        monster=monster_zones[possible_monsters[i]].get_name(), 
                        stat=monster_zones[possible_monsters[i]].get_stat(), 
                        pos=monster_zones[possible_monsters[i]].get_position()
                    ))
                monster_choice = try_int_input(
                    "Which card would you like to attack with: "
                )
                while (monster_choice >= len(possible_monsters) or 
                       monster_choice < 0):
                    monster_choice = try_int_input(
                        "Please enter a valid choice: "
                    )
                attacker = monster_zones[possible_monsters[monster_choice]]
                attacker_idx = possible_monsters[monster_choice]
                possible_targets = []
                possible_targets = opposite_player.get_field().get_monsters()
                opp_monster_zones = opposite_player.get_field().monster_zones
                if len(possible_targets):
                    for i in range(len(possible_targets)):
                        print("[{idx}] {monster} {stat} {pos}".format(
                            idx=i, 
                            monster=(
                                "???" if opp_monster_zones[possible_targets[i]]\
                                         .get_is_set() 
                                else opp_monster_zones[possible_targets[i]]\
                                     .get_name()
                            ), 
                            stat=(
                                "SET" if opp_monster_zones[possible_targets[i]]\
                                         .get_is_set() 
                                else opp_monster_zones[possible_targets[i]]\
                                     .get_stat()
                            ), 
                            pos=(
                                opp_monster_zones[possible_targets[i]].\
                                get_position()
                            )
                        ))
                    target_choice = try_int_input(
                        "Which card would you like to attack: "
                    )
                    while (target_choice >= len(possible_targets) or 
                           target_choice < 0):
                        target_choice = try_int_input(
                            "Please enter a valid choice: "
                        )
                    target = opp_monster_zones[possible_targets[target_choice]]
                    target_idx = possible_targets[target_choice]
                    battle_result = battle(attacker, target)
                    print(
                        "{attacker} [{attacker_stat} ATTACK] "
                        "ATTACKS {target} [{target_stat} {target_pos}]"\
                        .format(
                            attacker=attacker.get_name(), 
                            attacker_stat=attacker.get_atk(), 
                            target=target.get_name(), 
                            target_stat=target.get_stat(), 
                            target_pos=target.get_position()
                        )
                    )
                    # The following sections handle the logic of battle and 
                    # its result. Depending on the result of battle a monster
                    # may be destroyed, LifePoints may be lost, etc...

                    # This section handles the logic for the battle scenario
                    # in which the attacker wins against an Attack Position
                    # target.
                    if battle_result[0] and battle_result[1] > 0:
                        print(
                            "{attacker} WINS. {target} DESTROYED"\
                            .format(
                                attacker=attacker.get_name(), 
                                target=target.get_name()
                            )
                        )
                        opposite_player.get_gy().append(opposite_player\
                                                        .get_field()\
                                                        .remove(attacker_idx)
                        )
                        opposite_player.change_lp(-1 * battle_result[1])
                        attacker.lock_attack()
            
                    # This section handles the logic for the battle scenario
                    # in which the attacker loses against an Attack Position
                    # target.
                    elif battle_result[0] and battle_result[1] < 0:
                        print(
                            "{target} WINS. {attacker} DESTROYED"\
                            .format(
                                attacker=attacker.get_name(), 
                                target=target.get_name()
                            )
                        )
                        turn_player.get_gy().append(turn_player.get_field()\
                                                    .remove(target_idx)
                        )
                        turn_player.change_lp(battle_result[1])
            
                    # This section handles the logic for the battle scenario
                    # in which the attacker ties with an Attack Position 
                    # target.
                    elif battle_result[0] and battle_result[1] == 0:
                        print(
                            "BATTLE TIE. {attacker} and {target} DESTROYED"\
                            .format(
                                attacker=attacker.get_name(), 
                                target=target.get_name()
                            )
                        )
                        turn_player.get_gy().append(turn_player.get_field()\
                                                    .remove(attacker_idx)
                        )
                        opposite_player.get_gy().append(opposite_player\
                                                        .get_field()\
                                                        .remove(target_idx)
                        )
            
                    # This section handles the logic for the battle scenario
                    # in which the attacker loses to a Defense Position 
                    # target.
                    elif not battle_result[0] and battle_result[1] < 0:
                        print(
                            "{attacker} LOSES. {target} NOT DESTROYED"\
                            .format(
                                attacker=attacker.get_name(), 
                                target=target.get_name()
                            )
                        )
                        turn_player.change_lp(battle_result[1])
                        attacker.lock_attack()
                        if target.get_is_set():
                            target.flip()

                    # This section handles the logic for the battle scenario
                    # in which the attacker wins against a Defense Position 
                    # target.
                    elif not battle_result[0] and battle_result[1] > 0:
                        print(
                            "{attacker} WINS. {target} DESTROYED"\
                            .format(
                                attacker=attacker.get_name(), 
                                target=target.get_name()
                            )
                        )
                        opposite_player.get_gy().append(opposite_player\
                                                        .get_field()\
                                                        .remove(target_idx)
                        )
                        attacker.lock_attack()

                    # This section handles the logic for the battle scenario
                    # in which the attacker ties with a Defense Position 
                    # target.
                    else:
                        print("NO MONSTERS DESTROYED")
                        if target.get_is_set():
                            target.flip()
                        attacker.lock_attack()
                else:
                    # This section handles the logic for the battle scenario
                    # in which the opponent has no monsters and the attacker
                    # attacks directly.
                    print(
                        "{attacker} attacks Player {player} directly"\
                        .format(
                            attacker=attacker.get_name(), 
                            player=opposite_player.get_id()
                        )
                    )
                    damage = -1 * attacker.get_atk()
                    opposite_player.change_lp(damage)
                    attacker.lock_attack()
                # This section checks if either Players' LifePoints are 0
                # after battle. If one of the Players' LifePoints is 0 the
                # Duel ends and the other Player wins.
                if turn_player.get_lp() <= 0:
                    turn_player.set_lp(0)
                    winner = opposite_player.get_id()
                    break
                elif opposite_player.get_lp() <= 0:
                    opposite_player.set_lp(0)
                    winner = turn_player.get_id()
                    break

            # This section handles the logic for actions the Player can take
            # at any Phase in the Duel.
            # End Turn: Go to End Phase and start opponent's turn.
            elif possible_moves[choice] == "End Turn":
                phase = "EP"

            # This section clears the Player's possible actions and then adds
            # new possible actions based on the game state.
            # i.e. Game Phase, Turn Count, actions already taken, etc...
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
                # This section handles the logic of the End Phase.
                # If players have more than 6 cards they must discard down to
                # 6. The turn count is incremented and then the turn player
                # is changed the opposite player.
                while len(turn_player.get_hand()) > 6:
                    current_hand = turn_player.get_hand()
                    for i in range(len(current_hand)):
                        print(
                            "[{idx}] {card} [{attack} ATK / {defense} DEF]"\
                            .format(
                                idx=i, 
                                card=current_hand[i].get_name(), 
                                attack=current_hand[i].get_atk(), 
                                defense=current_hand[i].get_def()
                            )
                        )
                    choice = try_int_input(
                        "Too many cards in your hand. You have {}, you can "
                        "only have up to 6. Which card will you discard: ".\
                        format(len(current_hand))
                    )
                    while choice > len(current_hand) or choice < 0:
                        choice = try_int_input("Please enter a valid choice: ")
                    current_hand.pop(choice)
                turn_count += 1
                turn_player_idx = opposite_player_idx
            else:
                print("You shouldn't be here.")
    
    # After the Duel loop ends, the name of the winner is printed.
    print("PLAYER {} WINS!".format(winner))

if __name__ == '__main__':
    main()