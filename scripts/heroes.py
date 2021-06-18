import pygame, images, math, random
from constants import *
from scripts import Units



def init_tower_position(gf, tower_position, size):
	rect = 0
	if tower_position >= 1 and tower_position < 5:
		rect = gf.castle.castle_rect.y - 5*OBJECT_MULTIPLYER_HEIGHT - ((size[1]+5*OBJECT_MULTIPLYER_HEIGHT)) + CASTLE_SIZE[1]
	if tower_position >= 5 and tower_position < 9:
		rect = gf.castle.castle_rect.y - 5*OBJECT_MULTIPLYER_HEIGHT - ((size[1]+5*OBJECT_MULTIPLYER_HEIGHT)*2) + CASTLE_SIZE[1]
	return rect



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

		self.upgrade_cost = 600 + (150*self.level)
		self.stimpack_speed = FPS * 4 + (FPS*0.3*(self.level-1))

		self.rect = self.image.get_rect()
		self.init(gf)

	def init(self, gf):
		self.rect.x = gf.castle.castle_rect.x + 5*OBJECT_MULTIPLYER_WIDTH + ((self.size[0]+5*OBJECT_MULTIPLYER_WIDTH)*(self.tower_position-1))
		self.rect.y = init_tower_position(gf, self.tower_position, self.size)

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
			shooter.stimpack(self.stimpack_speed)

	def update(self, gf):
		if self.cooldown_iteration >= self.cooldown:
			self.cooldown_iteration = self.cooldown
		self.cooldown_bar_size = (math.ceil(HEROES_SIZE[0]*(self.cooldown_iteration/self.cooldown)), self.cooldown_bar_size[1])
		self.cooldown_bar_image = pygame.transform.scale(images.get_mana_bar(), self.cooldown_bar_size)
		self.cooldown_iteration += 1

	def new_level(self):
		self.level += 1
		self.upgrade_cost = 600 + (150*self.level)
		self.stimpack_speed = FPS * 4 + (FPS*0.3*(self.level-1))


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

		self.damage = level*12
		self.upgrade_cost = 600 + (150*self.level)

		self.rect = self.image.get_rect()
		self.init(gf)

	def init(self, gf):
		self.rect.x = gf.castle.castle_rect.x + 5*OBJECT_MULTIPLYER_WIDTH + ((self.size[0]+5*OBJECT_MULTIPLYER_WIDTH)*(self.tower_position-1))
		self.rect.y = init_tower_position(gf, self.tower_position, self.size)

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
			gf.allies_units.append(Units.FieldMaradauer(self.level, gf, row_position=i+1))

	def update(self, gf):
		if self.cooldown_iteration >= self.cooldown:
			self.cooldown_iteration = self.cooldown
		self.cooldown_bar_size = (math.ceil(HEROES_SIZE[0]*(self.cooldown_iteration/self.cooldown)), self.cooldown_bar_size[1])
		self.cooldown_bar_image = pygame.transform.scale(images.get_mana_bar(), self.cooldown_bar_size)
		self.cooldown_iteration += 1

	def new_level(self):
		self.level += 1
		self.damage = self.level*12
		self.upgrade_cost = 600 + (150*self.level)

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
		self.rect.y = init_tower_position(gf, self.tower_position, self.size)

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


class UnitHealer:
	def __init__(self, level, tower_position, gf):
		self.name = self.__class__.__name__
		self.image = images.get_unit_healer()
		self.level = level
		self.size = HEROES_SIZE
		self.ability_mana_cost = 210
		self.cooldown = FPS * 30
		self.cooldown_iteration = self.cooldown
		self.tower_position = tower_position

		self.heal = level*10
		self.upgrade_cost = 800 + (400*self.level)

		self.rect = self.image.get_rect()
		self.init(gf)

	def init(self, gf):
		self.rect.x = gf.castle.castle_rect.x + 5*OBJECT_MULTIPLYER_WIDTH + ((self.size[0]+5*OBJECT_MULTIPLYER_WIDTH)*(self.tower_position-1))
		self.rect.y = init_tower_position(gf, self.tower_position, self.size)

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
		for i in range(len(gf.allies_units)):
			if gf.allies_units[i].hp + self.heal <= gf.allies_units[i].total_hp:
				gf.allies_units[i].hp += self.heal
			else: gf.allies_units[i].hp = gf.allies_units[i].total_hp


	def update(self, gf):
		if self.cooldown_iteration >= self.cooldown:
			self.cooldown_iteration = self.cooldown
		self.cooldown_bar_size = (math.ceil(HEROES_SIZE[0]*(self.cooldown_iteration/self.cooldown)), self.cooldown_bar_size[1])
		self.cooldown_bar_image = pygame.transform.scale(images.get_mana_bar(), self.cooldown_bar_size)
		self.cooldown_iteration += 1

	def new_level(self):
		self.level += 1
		self.heal = self.level*10
		self.upgrade_cost = 800 + (400*self.level)



class RocketMan:
	def __init__(self, level, tower_position, gf):
		self.name = self.__class__.__name__
		self.image = images.get_rocket_man()
		self.level = level
		self.size = HEROES_SIZE
		self.ability_mana_cost = 45
		self.cooldown = FPS * 10
		self.cooldown_iteration = self.cooldown
		self.tower_position = tower_position

		self.damage = level*50
		self.upgrade_cost = 500 + (200*self.level)

		self.attacking = False
		self.target = None # position

		self.rect = self.image.get_rect()
		self.init(gf)

		self.total_shots = 5
		self.current_shot = 0

		self.shoot_speed = FPS
		self.shoot_iteration = 0

	def init(self, gf):
		self.rect.x = gf.castle.castle_rect.x + 5*OBJECT_MULTIPLYER_WIDTH + ((self.size[0]+5*OBJECT_MULTIPLYER_WIDTH)*(self.tower_position-1))
		self.rect.y = init_tower_position(gf, self.tower_position, self.size)

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
		gf.targetting_hero = self
		gf.start_targetting()


	def update(self, gf):
		if self.cooldown_iteration >= self.cooldown:
			self.cooldown_iteration = self.cooldown
		self.cooldown_bar_size = (math.ceil(HEROES_SIZE[0]*(self.cooldown_iteration/self.cooldown)), self.cooldown_bar_size[1])
		self.cooldown_bar_image = pygame.transform.scale(images.get_mana_bar(), self.cooldown_bar_size)
		self.cooldown_iteration += 1
		if self.attacking:
			if self.shoot_iteration >= self.shoot_speed:
				ch = random.randint(1, 2)
				if ch == 1:
					self.target = (self.target[0]+random.randint(0, 80), self.target[1])
				elif ch == 2 and not gf.castle.rect.collidepoint((self.target[0]-80, self.target[1])):
					self.target = (self.target[0]-random.randint(0, 80), self.target[1])
				self.shoot_iteration = 0
				gf.allies_units.append(Units.RocketBoom((self.target[0], gf.castle.rect.y+CASTLE_SIZE[1]-BLEW_SIZE[1]), gf, self.level))
				self.current_shot += 1
			if self.current_shot == self.total_shots:
				self.target = None
				self.attacking = False
				self.current_shot = 0

		self.shoot_iteration += 1


	def new_level(self):
		self.level += 1
		self.damage = self.level*50
		self.upgrade_cost = 500 + (200*self.level)

	def attack(self, gf):
		self.attacking = True
		self.target = (gf.hero_target_position[0], gf.hero_target_position[1])