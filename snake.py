#! /usr/bin/python

import pygame
import snake_utils as utils
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

# def rand_color():
#     return (randint(5, 255), randint(5, 255), randint(5, 255))

# # Class for creating multi-color text
# class MultiColorText:

#     def __init__(self, text, font):
#         self.chars = [font.render(c, True, rand_color()) for c in text]
#         self.char_w = self.chars[0].get_width()
#         self.char_h = self.chars[0].get_height()

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
        if self.body[0].block.x <= 0 or self.body[0].block.x >= SCREEN_WIDTH or self.body[0].block.y <= 0 or self.body[0].block.y >= SCREEN_HEIGHT:
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
        self.piece = pygame.Rect(randint(0, SCREEN_WIDTH - self.width), randint(0, SCREEN_HEIGHT - self.height), self.width, self.height)
        self.color = utils.rand_color()

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
        self.menu_options = ["play", "high_scores"]
        self.sel_option = 0
        self.sel_size = 10

    def menu(self):
        self.screen.fill((0, 0, 0))

        # Display the title text on the screen
        title_text = utils.MultiColorText("SNAKE", pygame.font.Font(r"resources\fonts\square-deal.ttf", 150))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), 10))

        # Display the play option on the screen
        title_text = utils.MultiColorText("PLAY", pygame.font.Font(r"resources\fonts\square-deal.ttf", 50))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), (SCREEN_HEIGHT / 2) - (title_text.full_text.get_height() / 2)))

        if (self.sel_option == 0):
            pygame.draw.rect(self.screen, utils.rand_color(), ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2) - (title_text.char_w), (SCREEN_HEIGHT / 2) - (title_text.full_text.get_height() / 2) + (title_text.char_h / 2) - self.sel_size, self.sel_size, self.sel_size))

        # Display the high-scores option on the screen
        title_text = utils.MultiColorText("HIGH SCORES", pygame.font.Font(r"resources\fonts\square-deal.ttf", 50))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), (SCREEN_HEIGHT / 2) + (title_text.full_text.get_height() / 2)))

        if (self.sel_option == 1):
            pygame.draw.rect(self.screen, utils.rand_color(), ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2) - (title_text.char_w), (SCREEN_HEIGHT / 2) + (title_text.full_text.get_height() / 2) + (title_text.char_h / 2) - self.sel_size, self.sel_size, self.sel_size))

        # Check for any events (button presses and Xing out)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.sel_option == 0:
                        self.state = "play"
                        self.snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        self.food = Food()
                    elif self.sel_option == 1:
                        print "Go to high scores page"
                elif event.key == pygame.K_UP:
                    if self.sel_option > 0:
                        self.sel_option -= 1
                    elif self.sel_option == 0:
                        self.sel_option = len(self.menu_options) - 1
                elif event.key == pygame.K_DOWN:
                    if self.sel_option < 1:
                        self.sel_option += 1
                    elif self.sel_option == len(self.menu_options) - 1:
                        self.sel_option = 0
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




SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400


clock = pygame.time.Clock()
is_running = True

game = Game()

while is_running:

    if game.state == "menu":
        fps = 10
        is_running = game.menu()
    elif game.state == "play":
        fps = 30
        is_running = game.run()

    pygame.display.flip()
    # Limit the frame rate to fps frames per second
    clock.tick(fps)

