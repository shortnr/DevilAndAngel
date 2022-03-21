from constants import *


class Robot:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def at_bomb(self, bomb):
        return self.x == bomb.x and self.y == bomb.y


class Bomb:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.color = GREEN
