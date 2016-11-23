#! /usr/bin/python

import pygame
from random import randint

def rand_color():
    return (randint(5, 255), randint(5, 255), randint(5, 255))

# Class for creating multi-color text
class MultiColorText:

    def __init__(self, text, font):
        self.chars = [font.render(c, True, rand_color()) for c in text]
        self.char_w = self.chars[0].get_width()
        self.char_h = self.chars[0].get_height()