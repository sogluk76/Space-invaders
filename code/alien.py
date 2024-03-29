import pygame

class Alien(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = './graphics/' + color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))

		if color == 'red': self.value = 100
		elif color == 'green': self.value = 200
		else: self.value = 400

		if color == 'red': self.life = 1
		elif color == 'green': self.life = 2
		else: self.life = 4

	def update(self,direction):
		self.rect.x += direction

class Extra(pygame.sprite.Sprite):
	def __init__(self,side,screen_width):
		super().__init__()
		self.image = pygame.image.load('./graphics/extra.png').convert_alpha()
		self.Evalue = 500
		
		if side == 'right':
			x = screen_width + 50
			self.speed = - 3
		else:
			x = -50
			self.speed = 3

		self.rect = self.image.get_rect(topleft = (x,80))

	def update(self):
		self.rect.x += self.speed