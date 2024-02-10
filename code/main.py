import pygame, sys
from time import sleep
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
 
class Game:

	def reset_game_for_next_level(self):

		# Player setup
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)
		

		# health and score setup
		self.display_live = min(self.lives - 1, 5)
		self.live_surf = pygame.image.load('./graphics/player.png').convert_alpha()
		self.live_x_start_pos = screen_width - ((self.live_surf.get_size()[0] + 10) * self.display_live)
		self.font = pygame.font.Font('./font/space_invaders.ttf',15)

		# Obstacle setup
		self.shape = obstacle.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.obstacle_amount = 4
		self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 480)

		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup(rows = 6, cols = 8)
		self.alien_direction = 1

		# Extra setup
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40,80)



	def __init__(self):

		# Initialisation du jeu
		self.is_victory = False
		self.level = 1
		
		# Player setup
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		# health and score setup
		self.lives = 3
		self.display_live = min(self.lives - 1, 5)
		self.live_surf = pygame.image.load('./graphics/player.png').convert_alpha()
		self.live_x_start_pos = screen_width - ((self.live_surf.get_size()[0] + 10) * self.display_live)
		self.score = 0
		self.highscore = 0
		self.font = pygame.font.Font('./font/space_invaders.ttf',15)

		# Obstacle setup
		self.shape = obstacle.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.obstacle_amount = 4
		self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 480)

		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup(rows = 6, cols = 8)
		self.alien_direction = 1

		# Extra setup
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40,80)

		# Audio
		music = pygame.mixer.Sound('./audio/music.wav')
		music.set_volume(0.05)
		music.play(loops = -1)
		self.laser_sound = pygame.mixer.Sound('./audio/laser.wav')
		self.laser_sound.set_volume(0.2)
		self.explosion_sound = pygame.mixer.Sound('./audio/explosion.wav')
		self.explosion_sound.set_volume(0.1)

		# name and Icon
		pygame.display.set_caption("Space Invader")
		self.icon = pygame.image.load('./graphics/ufo.png')
		pygame.display.set_icon(self.icon)


	def create_obstacle(self, x_start, y_start,offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index,col in enumerate(row):
				if col == 'x':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = obstacle.Block(self.block_size,(241,79,80),x,y)
					self.blocks.add(block)

	def create_multiple_obstacles(self,*offset,x_start,y_start):
		for offset_x in offset:
			self.create_obstacle(x_start,y_start,offset_x)

	def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				
				#level 1
				if self.level == 1:
					alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)
				
				#level 2
				if self.level == 2:
					if row_index == 0: alien_sprite = Alien('green',x,y)
					else: alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)
				
				#level 3
				if self.level == 3:
					if 0 <= row_index <= 1: alien_sprite = Alien('green',x,y)
					else: alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)
				
				#level 4
				if self.level == 4:
					if 0 <= row_index <= 2: alien_sprite = Alien('green',x,y)
					else: alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)

				#level 5
				if self.level == 5:
					if row_index == 0: alien_sprite = Alien('yellow',x,y)
					elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y)
					else: alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)
				
				#level 6
				if self.level == 6:
					if row_index == 0: alien_sprite = Alien('yellow',x,y)
					elif 1 <= row_index <= 3: alien_sprite = Alien('green',x,y)
					else: alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)
				
				#level 7
				if self.level == 7:
					if 0 <= row_index <= 1: alien_sprite = Alien('yellow',x,y)
					elif 2 <= row_index <= 3: alien_sprite = Alien('green',x,y)
					else: alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)

				#level 8
				if self.level == 8:
					if 0 <= row_index <= 1: alien_sprite = Alien('yellow',x,y)
					elif 2 <= row_index <= 4: alien_sprite = Alien('green',x,y)
					else: alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)

				#level 9
				if self.level == 9:
					if 0 <= row_index <= 2: alien_sprite = Alien('yellow',x,y)
					elif 2 <= row_index <= 4: alien_sprite = Alien('green',x,y)
					else: alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)

				#level 10
				if self.level >= 10:
					if 0 <= row_index <= 2: alien_sprite = Alien('yellow',x,y)
					elif 3 <= row_index <= 5: alien_sprite = Alien('green',x,y)
					else: alien_sprite = Alien('red',x,y)
					self.aliens.add(alien_sprite)				

	def alien_position_checker(self):
		all_aliens = self.aliens.sprites()
		for alien in all_aliens:
			if alien.rect.right >= screen_width:
				self.alien_direction = -1
				self.alien_move_down(2)
			elif alien.rect.left <= 0:
				self.alien_direction = 1
				self.alien_move_down(2)

	def alien_move_down(self,distance):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.rect.y += distance

	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center,6,screen_height)
			self.alien_lasers.add(laser_sprite)
			self.laser_sound.play()

	def extra_alien_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <= 0:
			self.extra.add(Extra(choice(['right','left']),screen_width))
			self.extra_spawn_time = randint(400,800)

	def collision_checks(self):

		# player lasers 
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
					

				# alien collisions
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,False)
				if aliens_hit:
					for alien in aliens_hit:
						alien.life -= 1	
						if alien.life <= 0:
							self.score += alien.value
							alien.kill()
							self.explosion_sound.play()
						laser.kill()

				# extra collision
				if pygame.sprite.spritecollide(laser,self.extra,True):
					self.score += 500
					self.lives += 1
					self.display_live = min(self.lives - 1, 5)
					self.live_x_start_pos = screen_width - ((self.live_surf.get_size()[0] + 10) * self.display_live)
					laser.kill()

		# alien lasers 
		if self.alien_lasers:
			for laser in self.alien_lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()

				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.lives -= 1
					self.display_live = min(self.lives - 1, 5)
					self.live_x_start_pos = screen_width - ((self.live_surf.get_size()[0] + 10) * self.display_live)
					if self.lives <= 0:
						defeats_text = f"You lost to level {self.level}"
						defeats_surf = self.font.render(defeats_text, False, 'white')
						defeats_rect = defeats_surf.get_rect(center=(screen_width / 2, screen_height / 2))
						screen.blit(defeats_surf, defeats_rect)
						pygame.display.flip()  

						# Attendre 3 secondes
						start_time = pygame.time.get_ticks()
						while pygame.time.get_ticks() - start_time < 3000:  # 3000 ms = 3 secondes
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									pygame.quit()
									sys.exit()
						pygame.quit()
						sys.exit()

		# aliens
		if self.aliens:
			for alien in self.aliens:
				pygame.sprite.spritecollide(alien,self.blocks,True)

				if pygame.sprite.spritecollide(alien,self.player,False):
					pygame.quit()
					sys.exit()
	
	def display_lives(self):

		size_img = pygame.transform.scale(self.live_surf, (23, 23))
		self.display_live = min(self.lives - 1, 5)
		self.live_x_start_pos = screen.get_width() - self.display_live * (size_img.get_size()[0] + 10)
		wave_surf = self.font.render(f'wave: {self.level}',False,'YELLOW')
		for live in range(self.display_live):
			x = self.live_x_start_pos + (live * (size_img.get_size()[0] + 10))
			screen.blit(size_img, (x, 8))


	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}',False,'YELLOW')
		score_rect = score_surf.get_rect(topleft = (10,10))
		screen.blit(score_surf,score_rect)

	def display_wave(self):
		wave_surf = self.font.render(f'wave: {self.level}',False,'YELLOW')
		wave_rect = wave_surf.get_rect(topleft = (10,30))
		screen.blit(wave_surf,wave_rect)

	def display_highscore(self):
		wave_surf = self.font.render(f'Highscore: {self.highscore}',False,'YELLOW')
		wave_rect = wave_surf.get_rect(topleft = (10,50))
		screen.blit(wave_surf,wave_rect)

	def check_for_highscore(self):
		if self.score > self.highscore:
			self.highscore = self.score

			with open('highscore.txt', "w") as file:
				file.write(str(self.highscore))
				#print(self.highscore)
			

	def load_highscore(self):
		try:
			with open("highscore.txt", "r") as file:
				self.highscore = int(file.read())
		except FileNotFoundError:
			self.highscore = 0


	def victory_message(self):
		if not self.aliens.sprites():
			victory_text = f"You won level {self.level}"
			victory_surf = self.font.render(victory_text, False, 'white')
			victory_rect = victory_surf.get_rect(center=(screen_width / 2, screen_height / 2))
			screen.blit(victory_surf, victory_rect)
			self.level += 1
			pygame.display.flip()  # Rafraîchit l'écran pour afficher le message

			# Attendre 3 secondes
			start_time = pygame.time.get_ticks()
			while pygame.time.get_ticks() - start_time < 3000:  # 3000 ms = 3 secondes
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
			self.reset_game_for_next_level()
						

	def run(self):
		self.player.update()
		self.alien_lasers.update()
		self.extra.update()
		
		self.aliens.update(self.alien_direction)
		self.alien_position_checker()
		self.extra_alien_timer()
		self.collision_checks()
		
		self.player.sprite.lasers.draw(screen)
		self.player.draw(screen)
		self.blocks.draw(screen)
		self.aliens.draw(screen)
		self.alien_lasers.draw(screen)
		self.extra.draw(screen)
		self.display_lives()
		self.display_score()
		self.display_wave()
		self.victory_message()
		self.check_for_highscore()
		self.load_highscore()
		self.display_highscore()

class CRT:
	def __init__(self):
		self.tv = pygame.image.load('./graphics/tv.png').convert_alpha()
		self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))

	def create_crt_lines(self):
		line_height = 3
		line_amount = int(screen_height / line_height)
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1)

	def draw(self):
		self.tv.set_alpha(randint(75,90))
		self.create_crt_lines()
		screen.blit(self.tv,(0,0))

if __name__ == '__main__':
	pygame.init()
	screen_width = 800
	screen_height = 600
	screen = pygame.display.set_mode((screen_width,screen_height))
	background = pygame.image.load('./graphics/background.png')
	clock = pygame.time.Clock()
	game = Game()
	crt = CRT()

	ALIENLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ALIENLASER,800)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == ALIENLASER:
				game.alien_shoot()

		screen.fill((30,30,30))
		screen.blit(background, (0, 0))
		game.run()
		#crt.draw()
			
		pygame.display.flip()
		clock.tick(60)