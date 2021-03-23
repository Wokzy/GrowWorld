import pygame, images, math
from constants import *
from scripts import Units


class StimManager:
	def __init__(self, level, tower_position, gf):
		self.name = self.__class__.__name__
		self.image = images.get_stim_manager()
		self.level = level
		self.size = HEROES_SIZE
		self.ability_mana_cost = 60
		self.cooldown = FPS * 15
		self.cooldown_iteration = self.cooldown
		self.tower_position = tower_position

		self.rect = self.image.get_rect()
		self.init(gf)

	def init(self, gf):
		self.rect.x = gf.castle.castle_rect.x + 5*OBJECT_MULTIPLYER_WIDTH + ((self.size[0]+5*OBJECT_MULTIPLYER_WIDTH)*(self.tower_position-1))
		self.rect.y = gf.castle.castle_rect.y - 5*OBJECT_MULTIPLYER_HEIGHT - ((self.size[1]+5*OBJECT_MULTIPLYER_HEIGHT)*((self.tower_position//4)+1)) + CASTLE_SIZE[1]

		self.cooldown_bar_size = (HEROES_SIZE[0], 2*OBJECT_MULTIPLYER_HEIGHT)
		self.cooldown_bar_image = pygame.transform.scale(images.get_mana_bar(), self.cooldown_bar_size)
		self.cooldown_bar_rect = self.cooldown_bar_image.get_rect()
		self.cooldown_bar_rect.x = self.rect.x
		self.cooldown_bar_rect.y = self.rect.y - 2*OBJECT_MULTIPLYER_HEIGHT

		self.cooldown_background_bar_size = (HEROES_SIZE[0], 2*OBJECT_MULTIPLYER_HEIGHT)
		self.cooldown_background_bar_image = pygame.transform.scale(images.get_mana_bar_background(), self.cooldown_background_bar_size)
		self.cooldown_background_bar_rect = self.cooldown_background_bar_image.get_rect()
		self.cooldown_background_bar_rect.x = self.rect.x
		self.cooldown_background_bar_rect.y = self.rect.y - 2*OBJECT_MULTIPLYER_HEIGHT


	def action(self, gf):
		if gf.in_battle and self.cooldown_iteration >= self.cooldown:
			if gf.castle.mana - self.ability_mana_cost >= 0:
				gf.castle.mana -= self.ability_mana_cost
				self.cooldown_iteration = 0
				self.ability(gf)
		elif not gf.in_battle:
			gf.change_unit(self)

	def ability(self, gf):
		for shooter in gf.town_shooters:
			shooter.stimpack()

	def update(self, gf):
		if self.cooldown_iteration >= self.cooldown:
			self.cooldown_iteration = self.cooldown
		self.cooldown_bar_size = (math.ceil(HEROES_SIZE[0]*(self.cooldown_iteration/self.cooldown)), self.cooldown_bar_size[1])
		self.cooldown_bar_image = pygame.transform.scale(images.get_mana_bar(), self.cooldown_bar_size)
		self.cooldown_iteration += 1


class Maradauer:
	def __init__(self, level, tower_position, gf):
		self.name = self.__class__.__name__
		self.image = images.get_maradauer()
		self.level = level
		self.size = HEROES_SIZE
		self.ability_mana_cost = 90
		self.cooldown = FPS * 18
		self.cooldown_iteration = self.cooldown
		self.tower_position = tower_position

		self.rect = self.image.get_rect()
		self.init(gf)

	def init(self, gf):
		self.rect.x = gf.castle.castle_rect.x + 5*OBJECT_MULTIPLYER_WIDTH + ((self.size[0]+5*OBJECT_MULTIPLYER_WIDTH)*(self.tower_position-1))
		#print(self.rect.x, self.tower_position)
		self.rect.y = gf.castle.castle_rect.y - 5*OBJECT_MULTIPLYER_HEIGHT - ((self.size[1]+5*OBJECT_MULTIPLYER_HEIGHT)*((self.tower_position//4)+1)) + CASTLE_SIZE[1]

		self.cooldown_bar_size = (HEROES_SIZE[0], 2*OBJECT_MULTIPLYER_HEIGHT)
		self.cooldown_bar_image = pygame.transform.scale(images.get_mana_bar(), self.cooldown_bar_size)
		self.cooldown_bar_rect = self.cooldown_bar_image.get_rect()
		self.cooldown_bar_rect.x = self.rect.x
		self.cooldown_bar_rect.y = self.rect.y - 2*OBJECT_MULTIPLYER_HEIGHT

		self.cooldown_background_bar_size = (HEROES_SIZE[0], 2*OBJECT_MULTIPLYER_HEIGHT)
		self.cooldown_background_bar_image = pygame.transform.scale(images.get_mana_bar_background(), self.cooldown_background_bar_size)
		self.cooldown_background_bar_rect = self.cooldown_background_bar_image.get_rect()
		self.cooldown_background_bar_rect.x = self.rect.x
		self.cooldown_background_bar_rect.y = self.rect.y - 2*OBJECT_MULTIPLYER_HEIGHT

	def action(self, gf):
		if gf.in_battle and self.cooldown_iteration >= self.cooldown:
			if gf.castle.mana - self.ability_mana_cost >= 0:
				gf.castle.mana -= self.ability_mana_cost
				self.cooldown_iteration = 0
				self.ability(gf)
		elif not gf.in_battle:
			gf.change_unit(self)

	def ability(self, gf):
		for i in range(6):
			gf.allies_units.append(Units.FieldMaradauer(1, gf, row_position=i+1))

	def update(self, gf):
		if self.cooldown_iteration >= self.cooldown:
			self.cooldown_iteration = self.cooldown
		self.cooldown_bar_size = (math.ceil(HEROES_SIZE[0]*(self.cooldown_iteration/self.cooldown)), self.cooldown_bar_size[1])
		self.cooldown_bar_image = pygame.transform.scale(images.get_mana_bar(), self.cooldown_bar_size)
		self.cooldown_iteration += 1

class Nothing:
	def __init__(self, tower_position, gf):
		self.name = 'Nothing'
		self.image = images.get_hero_background()
		self.rect = self.image.get_rect()
		self.size = HEROES_SIZE
		self.tower_position = tower_position

		self.init(gf)

	def init(self, gf):
		self.rect.x = gf.castle.castle_rect.x + 5*OBJECT_MULTIPLYER_WIDTH + ((self.size[0]+5*OBJECT_MULTIPLYER_WIDTH)*(self.tower_position-1))
		self.rect.y = gf.castle.castle_rect.y - 5*OBJECT_MULTIPLYER_HEIGHT - ((self.size[1]+5*OBJECT_MULTIPLYER_HEIGHT)*((self.tower_position//4)+1)) + CASTLE_SIZE[1]

		self.cooldown_bar_size = (HEROES_SIZE[0], 2*OBJECT_MULTIPLYER_HEIGHT)
		self.cooldown_bar_image = pygame.transform.scale(images.get_mana_bar(), self.cooldown_bar_size)
		self.cooldown_bar_rect = self.cooldown_bar_image.get_rect()
		self.cooldown_bar_rect.x = self.rect.x
		self.cooldown_bar_rect.y = self.rect.y - 2*OBJECT_MULTIPLYER_HEIGHT

		self.cooldown_background_bar_size = (HEROES_SIZE[0], 2*OBJECT_MULTIPLYER_HEIGHT)
		self.cooldown_background_bar_image = pygame.transform.scale(images.get_mana_bar_background(), self.cooldown_background_bar_size)
		self.cooldown_background_bar_rect = self.cooldown_background_bar_image.get_rect()
		self.cooldown_background_bar_rect.x = self.rect.x
		self.cooldown_background_bar_rect.y = self.rect.y - 2*OBJECT_MULTIPLYER_HEIGHT

	def action(self, gf):
		if not gf.in_battle:
			gf.change_unit(self)

	def update(self, gf):
		pass

	def ability(self, gf):
		pass