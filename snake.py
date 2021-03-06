#! /usr/bin/python

import pygame
import shelve
import os
import snake_utils as utils
from random import randint

#### Setup globals ####

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Commonly used colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GOLD = (255, 223, 0)
BLACK = (0, 0, 0)

# Window dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400

# Resource paths
SNAKE_DIR = os.path.dirname(os.path.realpath(__file__))
FONT_FILE = SNAKE_DIR + r"\resources\fonts\square-deal.ttf"
SAVE_FILE = SNAKE_DIR + r"\resources\high_scores\scores"

# Initialize pygame and the font to be used for the score
pygame.init()

BIG_SCORE = pygame.font.SysFont("arial black", 350)

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
        self.speed = 30

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

        # Each time a peice of food is created change the iocn to match the color of the food
        icon.fill(self.color)
        pygame.display.set_icon(icon)

    # Draw the piece of food on the given surface
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.piece)

# Contains information about high scores
class Score:

    def __init__(self):
        self.name = "???"
        self.score = 0

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
        self.high_scores = [Score() for _ in xrange(5)]
        self.new_name = "???"
        self.new_name_index = 0

    # Function that displays the menu
    def menu(self):
        self.screen.fill((0, 0, 0))

        # Display the title text on the screen
        title_text = utils.MultiColorText("SNAKE", pygame.font.Font(FONT_FILE, 150))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), 10))

        # Display the play option on the screen
        title_text = utils.MultiColorText("PLAY", pygame.font.Font(FONT_FILE, 50))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), (SCREEN_HEIGHT / 2) - (title_text.full_text.get_height() / 2)))

        if (self.sel_option == 0):
            pygame.draw.rect(self.screen, utils.rand_color(), ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2) - (title_text.char_ws[0]), (SCREEN_HEIGHT / 2) - (title_text.full_text.get_height() / 2) + (title_text.char_h / 2) - self.sel_size, self.sel_size, self.sel_size))

        # Display the high-scores option on the screen
        title_text = utils.MultiColorText("HIGH SCORES", pygame.font.Font(FONT_FILE, 50))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), (SCREEN_HEIGHT / 2) + (title_text.full_text.get_height() / 2)))

        if (self.sel_option == 1):
            pygame.draw.rect(self.screen, utils.rand_color(), ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2) - (title_text.char_ws[0]), (SCREEN_HEIGHT / 2) + (title_text.full_text.get_height() / 2) + (title_text.char_h / 2) - self.sel_size, self.sel_size, self.sel_size))

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
                        self.state = "scores"
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

    # Function that runs when the game is being played
    def play(self):
        self.snake.move()

        if self.snake.crash():
            # If the new score is better than the lowest high score, and the new score to the high scores list
            if self.snake.score > self.high_scores[4].score:
                print "Crash!"
                self.state = "new_score"
            else:
                print "Crash!"
                self.state = "menu"

        # If the snake hits the food, create a new piece at a difference location
        # Also add onto the snake
        if self.snake.ate(self.food):
            self.snake.add(self.food.color)
            self.food = Food()
            # Every 10 scores, ramp up the speed
            if self.snake.score % 5 == 0:
                self.snake.speed += 2

        # First draw the black background
        self.screen.fill((0, 0, 0))
        
        # Print the score to the screen, underneath (before) the snake and food
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

    # Function that displays the high scores
    def scores(self):
        self.screen.fill((0, 0, 0))

        # Display the title text on the screen
        title_text = utils.MultiColorText("HIGH SCORES", pygame.font.Font(FONT_FILE, 100))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), 10))

        for i in xrange(5):
            # Display high scores on the screen
            title_text = utils.MultiColorText(str(self.high_scores[i].score).zfill(5) + " " + self.high_scores[i].name, pygame.font.Font(FONT_FILE, 50))
            self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), (SCREEN_HEIGHT * 0.30) + (i * title_text.char_h)))

        # Check for any events (button presses and Xing out)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = "menu"
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

        return True

    # Function for submitting a new high score
    def new_score(self):
        self.screen.fill((0, 0, 0))

        # Display the title text on the screen
        title_text = utils.MultiColorText("NEW HIGH SCORE!", pygame.font.Font(FONT_FILE, 80))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), 10))

        # Display the instruction text on the screen
        title_text = utils.MultiColorText("Enter name below", pygame.font.Font(FONT_FILE, 50))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), (SCREEN_HEIGHT * 0.30)))

        # Display the name on the screen
        title_text = utils.MultiColorText(self.new_name, pygame.font.Font(FONT_FILE, 50))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), (SCREEN_HEIGHT * 0.50)))

        # Display the instruction text on the screen
        title_text = utils.MultiColorText("and press enter", pygame.font.Font(FONT_FILE, 50))

        self.screen.blit(title_text.full_text, ((SCREEN_WIDTH / 2) - (title_text.full_text.get_width() / 2), (SCREEN_HEIGHT * 0.70)))

        # Check for any events (button presses and Xing out)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # When the name is entered update the correct score
                if event.key == pygame.K_RETURN:
                    found_new_score_pos = False
                    prev_name = ""
                    prev_score = 0
                    for s in self.high_scores:

                        # Once the position for the new high score has been found, shift the scores below it down
                        if found_new_score_pos:
                            # Save the score and name before they are overwritten so they can be passed down to the next spot
                            tmp_prev_name = s.name
                            tmp_prev_score = s.score
                            s.name = prev_name
                            s.score = prev_score
                            prev_name = tmp_prev_name
                            prev_score = tmp_prev_score

                        if self.snake.score > s.score and not found_new_score_pos:
                            # Save the score and name before they are overwritten so they can be passed down to the next spot
                            prev_name = s.name
                            prev_score = s.score
                            s.name = self.new_name
                            s.score = self.snake.score
                            # Reset the new name and index
                            self.new_name = "???"
                            self.new_name_index = 0
                            # Set the flag to shift the rest of the high scores down
                            found_new_score_pos = True

                    # Switch to the high-scores list
                    self.state = "scores"
                elif (event.key == pygame.K_ESCAPE or 
                     event.key == pygame.K_UP or 
                     event.key == pygame.K_DOWN or 
                     event.key == pygame.K_RIGHT or 
                     event.key == pygame.K_LEFT):
                    # Don't do anything if escape is pressed
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    # Move the cursor back one
                    if self.new_name_index > 0:
                        self.new_name_index -= 1
                        tmp_str = list(self.new_name)
                        tmp_str[self.new_name_index] = "?"
                        self.new_name = "".join(tmp_str)
                else:
                    # Only add the input character if it's an alphanumeric and if the name is not already full
                    if pygame.key.name(event.key).isalnum() and self.new_name_index < 3:
                        # Add the typed character
                        # Need to create a new string because strings are immutable (can't be changed in place)
                        tmp_str = list(self.new_name)
                        tmp_str[self.new_name_index] = pygame.key.name(event.key)
                        self.new_name = "".join(tmp_str)
                        self.new_name_index += 1

        return True



clock = pygame.time.Clock()
pygame.display.set_caption("snake")

# Set the icon to be a square of random color
icon = pygame.Surface((32, 32))
icon.fill(utils.rand_color())
pygame.display.set_icon(icon)

# Initialize the state of the game to running
is_running = True

game = Game()
# Load the high scores from the save file
if (os.path.isfile(SAVE_FILE)):
    # Open the file if it already exists
    shelf_file = shelve.open(SAVE_FILE)
    game.high_scores = shelf_file['high_scores']
    shelf_file.close()
# Make sure that the snake directory is being found correctly
elif (os.path.isdir(SNAKE_DIR)):
    # Create the save file, and initialize it
    shelf_file = shelve.open(SAVE_FILE)
    shelf_file['high_scores'] = game.high_scores
    shelf_file.close()


while is_running:

    if game.state == "menu":
        fps = 10
        is_running = game.menu()
    elif game.state == "play":
        fps = game.snake.speed
        is_running = game.play()
    elif game.state == "scores":
        fps = 10
        is_running = game.scores()
    elif game.state == "new_score":
        fps = 10
        is_running = game.new_score()

    # If the game is being quit then save the current high scores
    if (not is_running):
        shelf_file = shelve.open(SAVE_FILE)
        shelf_file['high_scores'] = game.high_scores
        shelf_file.close()

    pygame.display.flip()
    # Limit the frame rate to fps frames per second
    clock.tick(fps)

