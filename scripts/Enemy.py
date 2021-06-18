import pygame, images, random, math
from constants import *
from datetime import datetime


class Enemy:
	def __init__(self, type_surface, type_damage, hp, speed, damage, attack_speed, image, size, wave, row_position=1, attack_range=60):
		self.type_surface = type_surface # Ground / Air
		self.type_damage = type_damage # Range / Melee
		self.total_hp = hp
		self.speed = speed # Speed of unit in pixels
		self.damage = damage # Damage in points
		self.attack_speed = attack_speed # Attack speed in iterations
		self.image = image
		self.rect = self.image.get_rect()
		self.size = size
		self.row_position = row_position # 1 - 6 position
		self.attack_range = attack_range # Espessially for 'Range' units

		self.hp_bar_image = images.get_hp_bar()
		self.hp_bar_size = (self.size[0], 5*OBJECT_MULTIPLYER_HEIGHT)
		self.hp_bar_image = pygame.transform.scale(self.hp_bar_image, self.hp_bar_size)
		self.hp_bar_rect = self.hp_bar_image.get_rect()

		self.hp_bar_background_image = images.get_hp_bar_background()
		self.hp_bar_background_size = self.hp_bar_size
		self.hp_bar_background_image = pygame.transform.scale(self.hp_bar_background_image, self.hp_bar_background_size)
		self.hp_bar_background_rect = self.hp_bar_background_image.get_rect()

		self.hp = self.total_hp
		self.rect.x = WIDTH
		self.rect.y = HEIGHT - self.size[1] - 120 * AVERAGE_MULTIPLYER + (row_position * 8 * AVERAGE_MULTIPLYER)
		self.alive = True

		self.attacking_me_shooters = 0
		self.attack_iteration = 0

		self.cost = 10 + (wave // 4)

		self.target = None

	def update(self, castle, gf):
		self.attack_iteration += 1
		if self.target != None and self.target.hp <= 0:
			self.target = None
		if self.target == None:
			self.find_target(gf)
		if self.hp <= 0:
			self.alive = False
			gf.gold += self.cost + ((self.cost // 100) * gf.bonus_gold)
			print(self.cost + ((self.cost // 100) * gf.bonus_gold))
			return None
		if self.type_damage == 'Melee':
			if not self.rect.colliderect(self.target.rect):
				self.rect.x -= self.speed
			elif self.rect.colliderect(self.target.rect):
				return self.attack()
			else: return ['Stay']
		elif self.type_damage == 'Range':
			if not self.rect.collidepoint(self.target.rect.x + self.attack_range):
				self.rect.x -= self.speed
			elif self.rect.collidepoint(self.target.rect.x + self.attack_range):
				return self.attack()
			else: return ['Stay']

		self.hp_bar_rect.x = self.rect.x
		self.hp_bar_rect.y = self.rect.y - self.hp_bar_size[1]*2

		self.hp_bar_background_rect.x = self.rect.x
		self.hp_bar_background_rect.y = self.rect.y - self.hp_bar_background_size[1]*2

		self.hp_bar_size = (math.ceil(self.size[0] - (self.total_hp - self.hp)*(self.size[0]/self.total_hp)), self.hp_bar_size[1])
		self.hp_bar_image = pygame.transform.scale(self.hp_bar_image, self.hp_bar_size)


	def attack(self):
		if self.attack_iteration >= self.attack_speed:
			self.attack_iteration = 0
			return ['Attack', self.damage]
		else:
			return ['Stay']

	def bite(self, dmg):
		self.hp -= dmg

	def find_target(self, gf):
		if len(gf.allies_units) > 0:
			while self.target == None or self.target != gf.castle and self.target.type_surface == 'Boom':
				self.target = random.choice([gf.castle, random.choice(gf.allies_units)])
		else: self.target = gf.castle



def monster(wave, row_position):
	return Enemy('Ground', 'Melee', ((wave//3)+1)*250, random.randint(2, 4)*AVERAGE_MULTIPLYER, 15, FPS*0.4, images.get_monster(), MONSTER_SIZE, wave, row_position=row_position)

def range_monster(wave, row_position):
	return Enemy('Ground', 'Range', ((wave//3)+1)*200, random.randint(1, 3)*AVERAGE_MULTIPLYER, 10, FPS*0.25, images.get_range_monster(), RANGE_MONSTER_SIZE, wave, row_position=row_position, attack_range=90)