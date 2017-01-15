#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from contextlib import contextmanager

import pygame

from .config import *
from .utils.display import get_font
from .scene.basic_scenes import *

__author__ = 'fyabc'


class Game:
    def __init__(self):
        # Initialize pygame.
        pygame.init()
        self.main_window = pygame.display.set_mode(WindowSize)
        self.timer = pygame.time.Clock()
        self.gFont = get_font()

        pygame.display.set_caption(GameTitle)

        # Game initialize.
        self.previous_scene_id = None
        self.current_scene_id = 0
        self.args_between_scenes = []
        self.scenes = {}

        # # For debug
        # from .scene.level_scene import LevelScene
        # self.scenes[0] = LevelScene.from_game_group(self, 'basic')[0]
        # # End debug

        scene_map = {
            'MainMenu': 0,
            'HelpMenu': 1,
            'GameSelectMenu': 2,
            'LevelSelectMenu': 3,
        }

        self.add_scene(0, MainMenu, scene_map)
        self.add_scene(1, HelpMenu)
        self.add_scene(2, GameSelectMenu, scene_map)
        self.add_scene(3, LevelSelectMenu, scene_map)

    @contextmanager
    def _game_manager(self):
        yield

        pygame.quit()

        # Save some data of the game.

        print('The game is quited!')
        sys.exit(0)

    def add_scene(self, scene_id, scene_type, *args, **kwargs):
        self.scenes[scene_id] = scene_type(self, scene_id, *args, **kwargs)

    def run(self):
        with self._game_manager():
            while True:
                scene = self.scenes[self.current_scene_id]

                result = scene.run(self.previous_scene_id, *self.args_between_scenes)

                if hasattr(result, '__len__'):
                    next_scene_id, *self.args_between_scenes = result
                else:
                    next_scene_id = result
                    self.args_between_scenes = []

                if next_scene_id == MainMenu.QuitID:
                    break

                self.previous_scene_id, self.current_scene_id = self.current_scene_id, next_scene_id
