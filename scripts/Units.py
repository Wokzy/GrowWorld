import pygame, images, random, math
from constants import *


class FieldMaradauer:
	def __init__(self, level, gf, row_position=1):
		self.type_surface = 'Ground' # Ground / Air
		self.type_damage = 'Range' # Range / Melee
		self.total_hp = level * 40
		self.level = level
		self.speed = 3 # Speed of unit in pixels
		self.damage = level*20 # Damage in points
		self.attack_speed = FPS * 0.85 # Attack speed in iterations

		self.attack_range = 120 * OBJECT_MULTIPLYER_WIDTH # range in pixels

		self.images = images.get_field_maradauer()
		self.stay_image = self.images['stay_image']
		self.shoot_images = self.images['shoot_image']
		self.image = self.stay_image

		self.rect = self.image.get_rect()
		self.size = FIELDMARADAUER_SIZE
		self.row_position = row_position # 1 - 6 position

		self.hp_bar_image = images.get_hp_bar()
		self.hp_bar_size = (self.size[0], 5*OBJECT_MULTIPLYER_HEIGHT)
		self.hp_bar_image = pygame.transform.scale(self.hp_bar_image, self.hp_bar_size)
		self.hp_bar_rect = self.hp_bar_image.get_rect()

		self.hp_bar_background_image = images.get_hp_bar_background()
		self.hp_bar_background_size = self.hp_bar_size
		self.hp_bar_background_image = pygame.transform.scale(self.hp_bar_background_image, self.hp_bar_background_size)
		self.hp_bar_background_rect = self.hp_bar_background_image.get_rect()

		self.hp = self.total_hp
		self.rect.x = gf.castle.castle_rect.x + CASTLE_SIZE[0]
		self.rect.y = HEIGHT - self.size[1] - 125 * AVERAGE_MULTIPLYER + (row_position * 8 * AVERAGE_MULTIPLYER)
		self.alive = True

		self.attack_iteration = 0
		self.target = None
		self.action = 'stay'

		self.animation_iterations = 0
		self.animation_speed = FPS * 0.3

		self.hp_iteration = 0
		self.hp_speed = FPS * 0.2

	def update(self, gf):
		if self.hp <= 0:
			self.alive = False
			return 'stay'
		if self.target != None and (self.target not in gf.battle_heroes and self.target != gf.boss or self.target.alive == False):
			self.target = None
		if self.target == None:
			self.action = 'stay'
			self.find_target(gf)
		else:
			if self.target.rect.x - self.rect.x <= self.attack_range:
				self.action = 'attack'
			else:
				self.rect.x += self.speed
				self.action = 'stay'

		if self.action == 'stay' and self.image != self.stay_image:
			self.image = self.stay_image
		elif self.action == 'attack':
			if self.image == self.stay_image:
				self.image = self.shoot_images[0]
			if self.animation_iterations >= self.animation_speed:
				if self.shoot_images.index(self.image) +1 < len(self.shoot_images):
					self.image = self.shoot_images[self.shoot_images.index(self.image) + 1]
				else:
					self.image = self.shoot_images[0]
				self.animation_iterations = 0

		self.attack_iteration += 1
		self.animation_iterations += 1

		self.hp_bar_rect.x = self.rect.x
		self.hp_bar_rect.y = self.rect.y - self.hp_bar_size[1]*2

		self.hp_bar_background_rect.x = self.rect.x
		self.hp_bar_background_rect.y = self.rect.y - self.hp_bar_background_size[1]*2

		self.hp_bar_size = (math.ceil(self.size[0] - (self.total_hp - self.hp)*(self.size[0]/self.total_hp)), self.hp_bar_size[1])
		self.hp_bar_image = pygame.transform.scale(self.hp_bar_image, self.hp_bar_size)

		if self.hp_iteration >= self.hp_speed:
			self.hp -= 1*self.level
			self.hp_iteration = 0

		self.hp_iteration += 1

		return self.action

	def find_target(self, gf):
		if gf.boss != None:
			self.target = gf.boss
		elif len(gf.battle_heroes) > 0:
			self.target = random.choice(gf.battle_heroes)
		else: self.target = None


class RocketBoom:
	def __init__(self, position, gf, level):
		self.type_surface = 'Boom' # Ground / Air
		self.type_damage = 'Boom' # Range / Melee
		self.level = level
		self.damage = level*50 # Damage in points

		self.attack_radius = 50 * OBJECT_MULTIPLYER_WIDTH # range in pixels

		self.images = images.get_rocket_boom()
		self.image = self.images[0]

		self.rect = self.image.get_rect()
		self.size = ROCKETBOOM_SIZE

		self.rect.x = position[0]
		self.rect.y = position[1]
		self.alive = True


		self.animation_iterations = 0
		self.animation_speed = FPS * 0.4

		self.attacked = False


	def update(self, gf):
		if self.animation_iterations >= self.animation_speed and self.alive:
			if self.images.index(self.image) +1 < len(self.images):
				self.image = self.images[self.images.index(self.image) + 1]
			else:
				self.image = self.images[0]
				self.alive = False
				return 'stay'
			self.animation_iterations = 0

		if not self.attacked:
			self.attack(gf)

		self.animation_iterations += 1

		return 'stay'

	def attack(self, gf):
		self.attacked = True

		for i in range(len(gf.battle_heroes)):
			if gf.battle_heroes[i].rect.colliderect(self.rect):
				gf.battle_heroes[i].hp -= self.damage