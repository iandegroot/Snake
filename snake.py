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
TITLE = pygame.font.SysFont("arial black", 50)

# Contains the coordinates of each individual part of the snake
class Segment:

	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init
		# Just in case a rainbow snake is wanted
		self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

# Contains everything that the snake does
class Snake:

	def __init__(self, x, y):
		self.size = 10
		self.seg_size = 5
		self.body = [pygame.Rect(x, y + (i * self.seg_size), self.seg_size, self.seg_size) for i in xrange(self.size)]
		self.hdir = 0
		self.vdir = -1
		self.increase_size = 10
		self.score = 0
		self.color = WHITE

	# Sets the direction of the snake
	def direction(self, dir):
		self.hdir, self.vdir = dir

	# Move the snake one block forward in the currently selected direction
	def move(self):
		for i in xrange(self.size - 1, 0, -1):
			self.body[i].clamp_ip(self.body[i - 1])

		self.body[0].move_ip(self.hdir * self.seg_size, self.vdir * self.seg_size)


	# Draw each segment of the snake on the given surface
	def draw(self, surface):
		for seg in self.body:
			pygame.draw.rect(surface, self.color, seg)

	# Check if the snake has crashed into itself or the walls, return True if it has
	def crash(self):
		if self.body[0].x <= 0 or self.body[0].x >= screen_width or self.body[0].y <= 0 or self.body[0].y >= screen_height:
			return True

		# Check if the snake hit itself
		for i in xrange(1, self.size):
			if self.body[0].colliderect(self.body[i]):
				return True

		return False

	# Check if the snake has collided with a piece of food
	def ate(self, food):
		if food.piece.colliderect(self.body[0]):
			return True
		else:
			return False

	# After the snake has eaten a piece of food increment the score, and make the snake bigger
	def add(self):
		self.score += 1
		self.size += self.increase_size
		for _ in xrange(self.increase_size):
			#temp_rect = pygame.Rect(self.body[2].x, self.body[2].x, self.seg_size, self.seg_size)
			temp_rect = pygame.Rect(-10, -10, self.seg_size, self.seg_size)
			self.body.append(temp_rect)


# Contains everything for the pieces of food that are eaten by the snake
class Food:

	def __init__(self):
		self.width = 8
		self.height = 8
		self.piece = pygame.Rect(randint(0, screen_width - self.width), randint(0, screen_height - self.height), self.width, self.height)
		self.color = (randint(5, 255), randint(5, 255), randint(5, 255))

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

	def menu(self, menu_text, mt_w, mt_h):
		self.screen.fill((0, 255, 0))

		self.screen.blit(menu_text, ((screen_width / 2) - (mt_w / 2), (screen_height / 2) - (mt_h / 2)))
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
			self.snake.add()
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

menu_title = TITLE.render("Press enter to play", True, BLACK)
mt_w = menu_title.get_width()
mt_h = menu_title.get_height()

while is_running:

	if game.state == "menu":
		is_running = game.menu(menu_title, mt_w, mt_h)


	elif game.state == "play":
		is_running = game.run()

	pygame.display.flip()
	# Limit the frame rate to 30 frames per second
	clock.tick(30)

