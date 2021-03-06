#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_event import GameEvent
from .death_events import MinionDeath, HeroDeath
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class Damage(GameEvent):
    def __init__(self, game, source, target, value):
        super(Damage, self).__init__(game)
        self.source = source
        self.target = target
        self.value = value

    def __str__(self):
        return '{}({}=>{}, value={})'.format(super().__str__(), self.source, self.target, self.value)

    def _happen(self):
        died = self.target.take_damage(self.source, self.value, self)

        if self.alive:
            self._message()

        if died:
            verbose('{} kill {}!'.format(self.source, self.target))
            # todo: add `MinionDeath` event
            if self.target in self.game.players:
                # Target is hero: hero death
                self.game.add_event_quick(HeroDeath, self.target)
            else:
                # Target is minion: minion death
                self.game.add_event_quick(MinionDeath, self.target)

    def _message(self):
        verbose('{} take {} damage to {}!'.format(self.source, self.value, self.target))


class SpellDamage(Damage):
    """This class represents damage from spell.

    Used to all 'Spell power +X' handlers.
    """

    def __init__(self, game, spell, target, value):
        super(SpellDamage, self).__init__(game, spell, target, value)

    @property
    def spell(self):
        return self.source


class RestoreHealth(GameEvent):
    def __init__(self, game, source, target, value):
        super().__init__(game)
        self.source = source
        self.target = target
        self.value = value

    def __str__(self):
        return '{}({}=>{}, value={})'.format(super().__str__(), self.source, self.target, self.value)

    def _happen(self):
        restored = self.target.restore_health(self.source, self.value, self)

        if restored:
            self._message()

    def _message(self):
        verbose('{} restore {} health to {}!'.format(self.source, self.value, self.target))


class GetArmor(GameEvent):
    def __init__(self, game, source, target, value):
        super().__init__(game)
        self.source = source
        self.target = target
        self.value = value

    def __str__(self):
        return '{}({}=>{}, value={})'.format(super().__str__(), self.source, self.target, self.value)

    def _happen(self):
        self._message()

        self.target.armor += self.value

    def _message(self):
        verbose('{} add {} armor to {}!'.format(self.source, self.value, self.target))


__all__ = [
    'Damage',
    'SpellDamage',
    'RestoreHealth',
    'GetArmor',
]
