# referenced: https://github.com/TimoWilken/flappy-bird-pygame

import pygame
from random import randint
from pygame.locals import *
from collections import deque
from ai import Net

pygame.init()
width, height = 500, 600
screen = pygame.display.set_mode((width, height))
gravity = .001

bird = pygame.image.load("bird.png")

class Bird(pygame.sprite.Sprite):
	WIDTH = HEIGHT = 80
	START_VELOCITY = .1
	STARTY = 200
	STARTX = 100

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.x, self.y = Bird.STARTX, Bird.STARTY
		self.image = pygame.image.load("bird.png")
		self.image = pygame.transform.scale(self.image, (Bird.WIDTH, Bird.HEIGHT))

		self.mask = pygame.mask.from_surface(self.image)

		self.velocity = .1

	def update(self):
		self.velocity += gravity
		self.y += self.velocity

	def flap(self):
		self.velocity -= Bird.START_VELOCITY * 10
		if self.velocity < -Bird.START_VELOCITY * 5:
			self.velocity = -Bird.START_VELOCITY * 5

	@property
	def rect(self):
		return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)

class Pipe(pygame.sprite.Sprite):
	PIECE_WIDTH = 80
	PIECE_HEIGHT = 30
	ADD_RATE = 1750
	SCROLL_SPEED = .2

	def __init__(self):
		self.x = width - 1
		self.image = pygame.Surface((Pipe.PIECE_WIDTH, height), SRCALPHA)
		self.counted = False

		self.image.convert()
		self.image.fill((0, 0, 0, 0))
		total_pieces = int((height - 3 * Bird.HEIGHT - 3 * Pipe.PIECE_HEIGHT)/Pipe.PIECE_HEIGHT)
		self.bot_pieces = randint(1, total_pieces)
		self.top_pieces = total_pieces - self.bot_pieces

		pipe_img = pygame.image.load("pipe.png")
		pipe_img = pygame.transform.scale(pipe_img, (Pipe.PIECE_WIDTH, 80))

		for i in range(self.bot_pieces + 1):
			piece_pos = (0, height - i * Pipe.PIECE_HEIGHT)
			self.image.blit(pipe_img, piece_pos)

		for i in range(self.top_pieces + 1):
			self.image.blit(pipe_img, (0, i * Pipe.PIECE_HEIGHT))

		self.top_pieces += 1
		self.bot_pieces += 1
		self.bot_height = self.bot_pieces * Pipe.PIECE_HEIGHT
		
		self.mask = pygame.mask.from_surface(self.image)
	
	@property
	def rect(self):
		return Rect(self.x, 0, Pipe.PIECE_WIDTH, Pipe.PIECE_HEIGHT)

	@property
	def visible(self):
		return -Pipe.PIECE_WIDTH < self.x < width

	def update(self):
		self.x -= Pipe.SCROLL_SPEED 

	def collides_with(self, bird):
		return pygame.sprite.collide_mask(self, bird)

def play(headless=False, ai=None):
	bird = Bird()
	pipes = deque()
	frame = 0
	score = 0
	done = False

	while True:
		# draw bird
		bird.update()
		if not headless:
			screen.fill((0, 255, 255))
			screen.blit(bird.image, (bird.x, bird.y))

		if frame % Pipe.ADD_RATE == 0:
			p = Pipe()
			pipes.append(p)

		col = any(p.collides_with(bird) for p in pipes)

		# check bounds
		if bird.y > 600 or bird.y < 0 or col:
			break

		while pipes and not pipes[0].visible:
			pipes.popleft()

		for p in pipes:
			if p.x + Pipe.PIECE_WIDTH/2 < bird.x and not p.counted:
				p.counted = True
				score += 1
                                print score

			p.update()
			if not headless:
				screen.blit(p.image, (p.x, 0))

		if not ai:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					break

				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					bird.flap()

		elif ai.forward([bird.x - pipes[0].x, height - bird.y - pipes[0].bot_height]) > 0.5:
			bird.flap()

		# update screen
		if not headless:
			pygame.display.flip()
		frame += 1

	print 'Score: ' + str(score)
	return score
