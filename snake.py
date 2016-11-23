#! /usr/bin/python

import pygame
from random import randint

# Setup globals
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GOLD = (255, 223, 0)
BLACK = (0, 0, 0)

# Initialize pygame and the font to be used for the score
pygame.init()

BIG_SCORE = pygame.font.SysFont("arial black", 350)
TEXT = pygame.font.Font(r"resources\fonts\square-deal.ttf", 150)

def rand_color():
    return (randint(5, 255), randint(5, 255), randint(5, 255))

# Class for creating multi-color text
class MultiColorText:

    def __init__(self, text):
        self.chars = [TEXT.render(c, True, rand_color()) for c in text]
        self.char_w = self.chars[0].get_width()
        self.char_h = self.chars[0].get_height()

# Contains the coordinates of each individual part of the snake
class Segment:

    def __init__(self, x_init, y_init, _color, _size):
        # Just in case a rainbow snake is wanted
        #self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = _color
        self.size = _size
        self.block = pygame.Rect(x_init, y_init, self.size, self.size)

# Contains everything that the snake does
class Snake:

    def __init__(self, x, y):
        self.size = 10
        self.seg_size = 5
        self.hdir = 0
        self.vdir = -1
        self.increase_size = 10
        self.score = 0
        self.color = WHITE
        #self.body = [pygame.Rect(x, y + (i * self.seg_size), self.seg_size, self.seg_size) for i in xrange(self.size)]
        self.body = [Segment(x, y + (i * self.seg_size), self.color, self.seg_size) for i in xrange(self.size)]

    # Sets the direction of the snake
    def direction(self, dir):
        self.hdir, self.vdir = dir

    # Move the snake one block forward in the currently selected direction
    def move(self):
        for i in xrange(self.size - 1, 0, -1):
            self.body[i].block.clamp_ip(self.body[i - 1].block)

        self.body[0].block.move_ip(self.hdir * self.seg_size, self.vdir * self.seg_size)


    # Draw each segment of the snake on the given surface
    def draw(self, surface):
        for seg in self.body:
            pygame.draw.rect(surface, seg.color, seg.block)

    # Check if the snake has crashed into itself or the walls, return True if it has
    def crash(self):
        if self.body[0].block.x <= 0 or self.body[0].block.x >= screen_width or self.body[0].block.y <= 0 or self.body[0].block.y >= screen_height:
            return True

        # Check if the snake hit itself
        for i in xrange(1, self.size):
            if self.body[0].block.colliderect(self.body[i].block):
                return True

        return False

    # Check if the snake has collided with a piece of food
    def ate(self, food):
        if food.piece.colliderect(self.body[0].block):
            return True
        else:
            return False

    # After the snake has eaten a piece of food increment the score, and make the snake bigger
    def add(self, color):
        self.score += 1
        self.size += self.increase_size
        for _ in xrange(self.increase_size):
            #temp_rect = pygame.Rect(self.body[2].x, self.body[2].x, self.seg_size, self.seg_size)
            #temp_rect = pygame.Rect(-10, -10, self.seg_size, self.seg_size)
            temp_seg = Segment(-10, -10, color, self.seg_size)
            self.body.append(temp_seg)


# Contains everything for the pieces of food that are eaten by the snake
class Food:

    def __init__(self):
        self.width = 8
        self.height = 8
        self.piece = pygame.Rect(randint(0, screen_width - self.width), randint(0, screen_height - self.height), self.width, self.height)
        self.color = rand_color()

    # Draw the piece of food on the given surface
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.piece)

class Game:

    def __init__(self):
        self.width = 640
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.snake = None
        self.food = None
        self.state = "menu"
        self.score_color = GRAY

    def menu(self, title_text):
        self.screen.fill((0, 0, 0))

        #self.screen.blit(menu_text, ((screen_width / 2) - (mt_w / 2), (15)))
        self.screen.blit(title_text.chars[0], ((screen_width / 2) - (title_text.char_w * 2.5), (10)))
        self.screen.blit(title_text.chars[1], ((screen_width / 2) - (title_text.char_w * 1.5), (10)))
        self.screen.blit(title_text.chars[2], ((screen_width / 2) - (title_text.char_w * 0.5), (10)))
        self.screen.blit(title_text.chars[3], ((screen_width / 2) + (title_text.char_w * 0.5), (10)))
        self.screen.blit(title_text.chars[4], ((screen_width / 2) + (title_text.char_w * 1.5), (10)))
        #screen.blit(menu_title, (50, 100))

        # Check for any events (button presses and Xing out)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = "play"
                    self.snake = Snake(screen_width / 2, screen_height / 2)
                    self.food = Food()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def run(self):
        self.snake.move()

        if self.snake.crash():
            print "Crash!"
            self.state = "menu"

        # If the snake hits the food, create a new piece at a difference location
        # Also add onto the snake
        if self.snake.ate(self.food):
            self.snake.add(self.food.color)
            self.food = Food()

        self.screen.fill((0, 0, 0))
        
        # Print the score to the screen, underneath (before) the snake and food
        if self.snake.score != 0 and self.snake.score % 10 == 0:
            self.score_color = GOLD
        else:
            self.score_color = GRAY
        label = BIG_SCORE.render(str(self.snake.score).zfill(2), True, self.score_color)
        self.screen.blit(label, (75, -65))

        # Draw the snake and the food to the screen
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # Check for any events (button presses and Xing out)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.vdir != 1:
                    self.snake.direction(UP)
                elif event.key == pygame.K_DOWN and self.snake.vdir != -1:
                    self.snake.direction(DOWN)
                elif event.key == pygame.K_LEFT and self.snake.hdir != 1:
                    self.snake.direction(LEFT)
                elif event.key == pygame.K_RIGHT and self.snake.hdir != -1:
                    self.snake.direction(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    return False

        return True




screen_width = 640
screen_height = 400


clock = pygame.time.Clock()
is_running = True

game = Game()

while is_running:

    if game.state == "menu":
        is_running = game.menu(MultiColorText("SNAKE"))


    elif game.state == "play":
        is_running = game.run()

    pygame.display.flip()
    # Limit the frame rate to 30 frames per second
    clock.tick(30)

