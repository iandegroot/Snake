#! /usr/bin/python

import pygame
from random import randint

def rand_color():
    return (randint(5, 255), randint(5, 255), randint(5, 255))

# Class for creating multi-color text
class MultiColorText:

    def __init__(self, text, font):
        self.chars = [font.render(c, True, rand_color()) for c in text]
        self.char_ws = [c.get_width() for c in self.chars]
        self.char_h = self.chars[0].get_height()
        self.num_small_chars = text.lower().count("l") + text.lower().count("i")
        self.num_big_chars = text.lower().count("m") + text.lower().count("w")
        self.full_text = pygame.Surface((sum(self.char_ws), self.char_h))

        # Blit each individual character onto the full_text surface, which will contain the whole word
        curr_left = 0
        for i in xrange(len(self.chars)):
            self.full_text.blit(self.chars[i], (curr_left, 0))

            curr_left += self.char_ws[i]

