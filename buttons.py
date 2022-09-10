import pygame


class Key:
    def __init__(self, key):
        self.key = key

    def pressed(self):
        return pygame.key.get_pressed()[self.key]


class Mod:
    def __init__(self, key):
        self.key = key

    def pressed(self):
        return pygame.key.get_mods() & self.key
