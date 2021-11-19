import pygame, images, random
from constants import *


class RedGiant:
	def __init__(self, level):
		self.level = level
		self.hp = 40000 + self.level * 5500
		self.max_hp = int(self.hp)
		self.damage = 100 + self.level * 50
		self.alive = True
		self.armor_multiplyer = 0.8 # Multiplyer for incoming damage

		self.attack_speed = FPS * .4
		self.attack_iteration = 0
		self.attack_animation_stage = 0

		self.imgs = images.get_red_giant()
		self.image = self.imgs['move'][0]

		self.move_speed = FPS * .4
		self.move_iteration = 0
		self.move_animation_stage = 0

		self.speed = 2*AVERAGE_MULTIPLYER

		self.rect = self.image.get_rect()
		self.rect.x = WIDTH
		self.rect.y = HEIGHT - 80*OBJECT_MULTIPLYER_HEIGHT - RED_GIANT_SIZE[1]

	def update(self, gf):
		if not gf.castle.rect.colliderect(self.rect):
			if self.move_iteration >= self.move_speed:

				if self.move_animation_stage == len(self.imgs['move']):
					self.move_animation_stage = 0

				self.image = self.imgs['move'][self.move_animation_stage]

				self.move_animation_stage += 1
				self.move_iteration = 0

			self.move_iteration += 1

			self.rect.x -= self.speed
		else:
			if self.attack_iteration >= self.attack_speed / 4:

				if self.attack_animation_stage == len(self.imgs['attack']):
					if gf.castle.hp - self.damage >= 0:
						gf.castle.hp -= self.damage
					else:
						gf.castle.hp = 0
					self.attack_animation_stage = 0

				self.image = self.imgs['attack'][self.attack_animation_stage]

				self.attack_animation_stage += 1
				self.attack_iteration = 0

			self.attack_iteration += 1