import pygame
from pygame.locals import *
import random

pygame.init()

# 709*630	# 739*138	(30)	# 63*450	# 42*30		# 99*35

screen_width = 709
screen_height = 768

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#Define Font
font = pygame.font.SysFont('Bauhaus 93', 50)

#Define Font Color
white = (255,255,255)

#Game Variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
time_start = pygame.time.get_ticks() - pipe_frequency
pipe_enter = False
counter = 0

#Load Images
bg = pygame.image.load('D:/Flappy Bird Pygame/Images/bg.png')
ground = pygame.image.load('D:/Flappy Bird Pygame/Images/ground.png')
button_img = pygame.image.load('D:/Flappy Bird Pygame/Images/restart.png')

#Counter
def draw_score(text, font, font_col, x, y):
	img = font.render(text, True, font_col)
	screen.blit(img, (x,y))

def reset_game():
	pipe_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height/2)
	counter = 0
	flappy.image = pygame.transform.rotate(flappy.image, 90)
	return counter

#Bird Class
class Bird(pygame.sprite.Sprite):
	#Storing all bird images 
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for i in range(1,5):
			img = pygame.image.load(f'D:/Flappy Bird Pygame/Images/bird{i}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
		self.vel = 0
		self.clicked = False

		#Bird flapping update
	def update(self):
		
		if flying == True:
			#Gravity
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if  self.rect.bottom < 630:
				self.rect.y += self.vel

			#Jumping
			if game_over == False:
				if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					self.clicked = True
					self.vel = -10
				if pygame.mouse.get_pressed()[0] == 0:
					self.clicked = False

			#Bird annimation
			self.cooldown = 3
			self.counter += 1

			if self.counter > self.cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]
		
			self.image = pygame.transform.rotate(self.images[self.index], self.vel*-2)

		if game_over == True:
			self.image = pygame.transform.rotate(self.images[self.index], -90)

#Pipe Class
class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('D:/Flappy Bird Pygame/Images/pipe.png')
		self.rect = self.image.get_rect()
		#Position 1 means Top and -1 means Bottom
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x,y-int(pipe_gap/2)]
		if position == -1:
			self.rect.topleft = [x,y+int(pipe_gap/2)]

	def update(self):
		if flying == True:
			self.rect.x -= scroll_speed
			if self.rect.right < 0:
				self.kill()

class Button():
	def __init__(self, x, y, picture):
		self.image = picture
		self.rect = self.image.get_rect()
		self.rect.topleft = [x,y]

	def draw(self): 
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check if mouse is over the button
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)

#Restart Button
button = Button(screen_width/2 - 50, screen_height/2 - 100, button_img)

run = True
while run:

	clock.tick(fps)

	#Background
	screen.blit(bg, (0,0))

	#Draw and update
	pipe_group.draw(screen)
	bird_group.draw(screen)	
	bird_group.update()

	#Draw ground
	screen.blit(ground, (ground_scroll,630))

	#Score Counter
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
		and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
		and pipe_enter == False:
			pipe_enter = True
		if 	pipe_enter == True and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
			pipe_enter = False
			counter += 1

	draw_score(str(counter), font, white, screen_width/2, 20)

	#Check  ision
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		game_over = True
	
	if flappy.rect.bottom >= 630:
		game_over = True
		flying = False

	if game_over == False and flying == True:
		#Pipe Generation
		time_now = pygame.time.get_ticks()
		if (time_now - time_start)> pipe_frequency:
			pipe_height = random.randint(-125,125)
			btm_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, 1)
			top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, -1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)		
			time_start = pygame.time.get_ticks()

		#Scrolling Ground
		ground_scroll -= scroll_speed
		if abs(ground_scroll)>30:
			ground_scroll=0
		pipe_group.update()		

	if game_over == True:
		if button.draw() == True:
			game_over = False
			counter = reset_game()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run=False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()