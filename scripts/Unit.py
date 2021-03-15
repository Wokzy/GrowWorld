import pygame, images, random, math
from constants import *
from datetime import datetime


class Enemy:
	def __init__(self, type_surface, type_damage, hp, speed, damage, attack_speed, image, size, row_position=1):
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

	def update(self, castle):
		self.attack_iteration += 1
		if self.hp <= 0:
			self.alive = False
			return None
		if self.type_damage == 'Melee':
			if not self.rect.colliderect(castle.castle_rect):
				self.rect.x -= self.speed
			elif self.rect.colliderect(castle.castle_rect):
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



def monster(wave, row_position):
	return Enemy('Ground', 'Melee', wave*100, random.randint(2, 4)*AVERAGE_MULTIPLYER, 15, FPS*0.4, images.get_monster(), MONSTER_SIZE, row_position)