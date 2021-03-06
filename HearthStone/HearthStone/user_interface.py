#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_events.basic_events import GameBegin, GameEnd, TurnEnd
from .game_events.play_events import SummonMinion
from .utils import verbose, error, Config
from .cli_tool import simple_show_board, show_board, clear_screen

__author__ = 'fyabc'

windowWidth = Config['CLI']['windowWidth']


class GameUserInterface:
    """The user interface of the game.

    It receives user actions, execute it with the "Game" it contains, and return result.
    User can observe game status from this interface.
    It can connect to GUI or CLI.
    """

    def __init__(self, game):
        self.game = game

    ############################################
    # Methods that get the status of the game. #
    ############################################

    def get_game(self):
        return self.game

    ########################################################################
    # Methods that take some operations and send some actions to the game. #
    ########################################################################

    def show(self):
        simple_show_board(self.game)

    def clear_screen(self):
        clear_screen()

    def game_begin(self):
        self.game.dispatch_event_quick(GameBegin)

    def game_end(self):
        self.game.dispatch_event_quick(GameEnd)

    def turn_end(self):
        self.game.dispatch_event_quick(TurnEnd)

    def try_play_card(self, index, *args):
        """

        :param index: The index in hand of the card you want to play.
        :param args: Other necessary arguments.
        :return: None
        """

        player = self.game.current_player

        if not 0 <= index < player.hand_number:
            error('This is not a valid card index (0 ~ {})!'.format(player.hand_number - 1))
            return

        card = player.hand[index]

        if player.remain_crystal < card.cost:
            error('I don\'t have enough mana crystals!')
            return

        if card.data.type == card.Type_Minion:
            self._try_summon_minion(player, card, *args)
        elif card.data.type == card.Type_Spell:
            pass
        elif card.data.type == card.Type_Weapon:
            pass

    def _try_summon_minion(self, player, minion, location):
        if player.desk_full:
            error('The desk of P{} is full!'.format(player.player_id))
            return

        if not 0 <= location <= player.desk_number:
            error('This is not a valid location (0 ~ {})!'.format(player.desk_number))
            return

        self.game.dispatch_event_quick(SummonMinion, minion, location, player.player_id)

    def try_attack(self, source_index, target_index):
        """Try to attack.

        [NOTE] source is always current player, target is always opponent.

        :param source_index: The index of source in desk (None means your hero)
        :param target_index: The index of target in desk (None means opponent's hero)
        :return: None
        """

        player = self.game.current_player
        opponent = self.game.opponent_player


__all__ = [
    'GameUserInterface',
]
