import pygame 

class Block(pygame.sprite.Sprite):
	def __init__(self,size,color,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft = (x,y))

shape = [
'00xxxxxxx00',
'0xxxxxxxxx0',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxx000xxxx',
'xxx00000xxx',
'xx0000000xx']