import pygame, images
from constants import *
from datetime import datetime


class TownShooter:
	def __init__(self, level, imgs, row, column):
		self.stay_image = imgs['stay_image']
		self.shoot_images = imgs['shoot_image']
		self.size = imgs['total_size']
		self.image = self.stay_image
		self.level = level
		self.damage = level*5

		self.rect = self.image.get_rect()
		self.x = (column*self.size[0] + 5*OBJECT_MULTIPLYER_WIDTH)
		self.y = (HEIGHT - 100*OBJECT_MULTIPLYER_HEIGHT - (row*self.size[1]))

		self.rect.x = self.x
		self.rect.y = self.y

		self.action = 'stay' # stay or attack
		self.target = None

		self.shoot_timer = datetime.now()
		self.animation_timer = datetime.now()

		self.attack_speed = 0.4

	def update(self, battle_units):
		if self.target != None:
			if self.target not in battle_units or self.target.hp <= 0:
				self.target = None
			else:
				if self.action != 'attack':
					self.action = 'attack'
		if self.target == None:
			if self.action != 'stay':
				self.action = 'stay'
			self.find_target(battle_units)
		if self.action == 'stay' and self.image != self.stay_image:
			self.image = self.stay_image
		elif self.action == 'attack':
			if self.image == self.stay_image:
				self.image = self.shoot_images[0]
			if (datetime.now() - self.animation_timer).total_seconds() >= 0.1:
				if self.shoot_images.index(self.image) +1 < len(self.shoot_images):
					self.image = self.shoot_images[self.shoot_images.index(self.image) + 1]
				else:
					self.image = self.shoot_images[0]

		if self.action == 'attack' and (datetime.now() - self.shoot_timer).total_seconds() < self.attack_speed:
			self.action = 'stay'
		elif self.action == 'attack' and (datetime.now() - self.shoot_timer).total_seconds() >= self.attack_speed:
			self.shoot_timer = datetime.now()

		return self.action

	def find_target(self, battle_units):
		target = None
		distance = WIDTH

		for enemy in battle_units:
			cur_distance = enemy.rect.x - self.rect.x
			if cur_distance < distance:
				if len(battle_units) <= 7:
					target = enemy
					distance = cur_distance
				elif len(battle_units) > 7 and enemy.attacking_me_shooters < 5:
					target = enemy
					distance = cur_distance

		if target != None:
			battle_units[battle_units.index(target)].attacking_me_shooters += 1
		self.target = target