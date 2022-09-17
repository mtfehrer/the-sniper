import pygame, sys, random, time

screen_size = (1200, 900)
screen_center = (screen_size[0] / 2, screen_size[1] / 2)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("The Sniper")
clock = pygame.time.Clock()
bird_img = pygame.image.load("flappy bird.png").convert_alpha()
mole_img = pygame.image.load("mole.png").convert_alpha()
scope_img = pygame.image.load("circle at center.png").convert_alpha()
scope_line_length = 3
shoot_cooldown = 200
ground_height1 = screen_size[1] / 3
ground_height2 = screen_size[1] / 1.75
ground_height3 = screen_size[1] / 1.25
bird_starting_pos = (screen_size[0], 145)
bird_size = (85, 70)
bird_speed = 2
bird_spawn_chance = 700
mole_spawn_chance = 200
mole_size = (100, 100)
mole_speed = 1
framerate = 144
time_in_seconds = 60
red = (255, 0, 0)
green = (0, 255, 0)
light_blue = (0, 181, 226)
black = (0, 0, 0)
light_green1 = (0, 150, 0)
light_green2 = (0, 100, 0)
light_green3 = (0, 50, 0)
white = (255, 255, 255)
background_color = light_blue
pygame.init()

gun_sound = pygame.mixer.Sound("sniper sound effect.mp3")
gun_sound.set_volume(0.1)
default_font = pygame.font.SysFont("arial", 70)
title_font = pygame.font.SysFont("comicsansms", 140)

score_text = default_font.render("Score:", True, white)

time_text = default_font.render("Time:", True, white)

title_text = title_font.render("The Sniper", True, black)
title_text_rect = title_text.get_rect(center=(screen_center[0], screen_center[1] / 2))

start_button = pygame.Surface((200, 100))
start_button_rect = start_button.get_rect(center=screen_center)
start_text = default_font.render("Start", True, black)
start_text_rect = start_text.get_rect(center=screen_center)

class Main:
	def __init__(self):
		self.bird_group = pygame.sprite.Group()
		self.mole_list = []
		self.shoot = False
		self.cooldown = shoot_cooldown
		self.score = 0
		self.title = True
		self.high_score = 0
		self.time_left = time_in_seconds * framerate
		self.elapsed_time = 0

	def get_mouse_details(self):
		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_press = pygame.mouse.get_pressed()
		self.mouse_rect = pygame.Rect(self.mouse_pos, (1, 1))

	def check_button_press(self):
		if start_button_rect.contains(self.mouse_rect):
			start_button.fill(red)
			if self.mouse_press[0] == True:
				self.title = False
		else:
			start_button.fill(green)

	def create_high_score(self):
		self.high_score_text = default_font.render("High Score: " + str(self.high_score), True, black)
		self.high_score_text_rect = self.high_score_text.get_rect(center=(screen_center[0], screen_center[1] * 1.5))

	def display_title_screen(self):
		screen.fill(background_color)
		screen.blit(title_text, title_text_rect)
		screen.blit(start_button, start_button_rect)
		screen.blit(start_text, start_text_rect)
		screen.blit(self.high_score_text, self.high_score_text_rect)

	def determine_shoot(self):
		if self.mouse_press[0] == True:
			if self.cooldown <= 0:
				self.shoot = True
				self.cooldown = shoot_cooldown
				gun_sound.play()
			else:
				self.shoot = False
		self.cooldown -= 1

	def generate_entities(self):
		#birds
		if random.randint(0, bird_spawn_chance) == 0:
			self.bird_group.add(Bird())
		#moles
		if random.randint(0, mole_spawn_chance) == 0:
			self.mole_list.append(Mole())

	def update_birds(self):
		self.bird_group.update()
		#check for out of bounds
		for bird in self.bird_group.sprites():
			if bird.rect.x < 0 - bird_size[0]:
				self.bird_group.remove(bird)

	def update_moles(self):
		for mole in self.mole_list:
			mole.update()
		#check for out of bounds
		for mole in self.mole_list:
			if mole.under == True:
				self.mole_list.remove(mole)

	def check_kill(self):
		#birds
		for bird in self.bird_group.sprites():
			if bird.rect.contains(self.mouse_rect):
				if self.shoot == True:
					self.bird_group.remove(bird)
					self.score += 1
		#moles
		for mole in self.mole_list:
			if mole.out_rect.contains(self.mouse_rect):
				if self.shoot == True:
					self.mole_list.remove(mole)
					self.score += 1

	def fill_screen(self):
		screen.fill(background_color)

	def display_grounds_and_moles(self):
		for mole in self.mole_list:
			if mole.ground == 1:
				screen.blit(mole.image, mole.rect)
		pygame.draw.rect(screen, light_green1, ((0, ground_height1), screen_size))

		for mole in self.mole_list:
			if mole.ground == 2:
				screen.blit(mole.image, mole.rect)
		pygame.draw.rect(screen, light_green2, ((0, ground_height2), screen_size))

		for mole in self.mole_list:
			if mole.ground == 3:
				screen.blit(mole.image, mole.rect)
		pygame.draw.rect(screen, light_green3, ((0, ground_height3), screen_size))

	def display_birds(self):
		self.bird_group.draw(screen)

	def display_scope(self):
		#horizontal line
		horizontal_line_surf = pygame.Surface((screen_size[0] * 2, scope_line_length))
		horizontal_line_surf.fill(red)
		horizontal_line_rect = horizontal_line_surf.get_rect(center=self.mouse_pos)
		screen.blit(horizontal_line_surf, horizontal_line_rect)
		#vertical line
		vertical_line_surf = pygame.Surface((scope_line_length, screen_size[1] * 2))
		vertical_line_surf.fill(red)
		vertical_line_rect = vertical_line_surf.get_rect(center=self.mouse_pos)
		screen.blit(vertical_line_surf, vertical_line_rect)
		#scope
		scope_rect = scope_img.get_rect(center=self.mouse_pos)
		screen.blit(scope_img, scope_rect)

	def display_score(self):
		screen.blit(score_text, (0, 0))
		score_num_text = default_font.render(str(self.score), True, white)
		screen.blit(score_num_text, (170, 0))

	def display_time(self):
		screen.blit(time_text, (0, 100))
		seconds = int(self.time_left / framerate) + 1
		time_num_text = default_font.render(str(seconds), True, white)
		screen.blit(time_num_text, (150, 100))

	def subtract_time(self):
		self.time_left -= 1

	def check_game_end(self):
		if self.time_left <= 0:
			self.title = True
			if self.score > self.high_score:
				self.high_score = self.score
			self.create_high_score()
			self.score = 0
			self.time_left = time_in_seconds * framerate

class Bird(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		flipped_img = pygame.transform.flip(bird_img, True, False)
		self.image = pygame.transform.scale(flipped_img, bird_size)
		self.rect = self.image.get_rect(center=bird_starting_pos)

	def move(self):
		self.rect.x -= bird_speed

	def update(self):
		self.move()

class Mole(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(mole_img, mole_size)
		self.ground = random.randint(1, 3)
		x = random.randint(mole_size[0], screen_size[0] - mole_size[0])
		if self.ground == 1: self.og_y = ground_height1
		if self.ground == 2: self.og_y = ground_height2
		if self.ground == 3: self.og_y = ground_height3
		self.rect = self.image.get_rect(topleft=(x, self.og_y))
		self.out_rect = None
		self.direction = "up"
		self.under = False

	def change_dir_and_check_under(self):
		if self.rect.y <= self.og_y - mole_size[1]:
			self.direction = "down"
		if self.rect.y >= self.og_y:
			self.under = True

	def set_out_rect(self):
		if self.ground == 1: new_height = ground_height1 - self.rect.y
		if self.ground == 2: new_height = ground_height2 - self.rect.y
		if self.ground == 3: new_height = ground_height3 - self.rect.y
		self.out_rect = pygame.Rect((self.rect.x, self.rect.y), (mole_size[0], new_height))

	def move(self):
		if self.direction == "up":
			self.rect.y -= mole_speed
		else:
			self.rect.y += mole_speed

	def update(self):
		self.move()
		self.change_dir_and_check_under()
		self.set_out_rect()

main = Main()
main.create_high_score()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	main.get_mouse_details()

	if main.title == True:
		main.check_button_press()
		main.display_title_screen()

	elif main.title == False:
		main.determine_shoot()
		main.generate_entities()
		main.update_birds()
		main.update_moles()
		main.check_kill()

		main.fill_screen()
		main.display_birds()
		main.display_grounds_and_moles()
		main.display_scope()
		main.display_score()
		main.display_time()
		main.subtract_time()
		main.check_game_end()

	pygame.display.update()
	clock.tick(framerate)