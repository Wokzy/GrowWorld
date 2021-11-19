import pygame, images, random
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
		self.target_is_boss = False

		self.shoot_iterations = 0
		self.animation_iterations = 0
		self.stimpack_iterations = 0
		self.stimpack_animation_iterations = 0

		self.default_attack_speed = FPS * 0.4
		self.default_animation_speed = FPS * 0.1
		self.attack_speed = self.default_attack_speed # in Iterations
		self.animation_speed = self.default_animation_speed # in Iterations
		self.stimpack_animation_speed = FPS
		self.stimpack_speed = None # in Iterations

		self.on_stimpack = False # stimpack - boost of shooting on STIMPACK_BUFF
		self.stimpack_animation = False

		self.upgrade_cost = int(600 + (600*0.15)*self.level)

	def update(self, battle_units, gf):
		if self.on_stimpack:
			if self.stimpack_iterations >= self.stimpack_speed:
				self.stop_stimpack()
				#print(f'stop stimpack! attack - {self.attack_speed}; animation - {self.animation_speed}')
			else:
				self.stimpack_iterations += 1
		if self.target != None:
			if self.target not in battle_units and self.target_is_boss == False or self.target.alive == False:
				self.target = None
			else:
				if self.action != 'attack':
					self.action = 'attack'
		if self.target == None:
			if self.action != 'stay':
				self.action = 'stay'
			self.find_target(battle_units, gf)
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


		if self.action == 'attack' and self.shoot_iterations < self.attack_speed:
			self.action = 'stay'
		elif self.action == 'attack' and self.shoot_iterations >= self.attack_speed:
			self.shoot_iterations = 0

		self.animation_iterations += 1
		self.shoot_iterations += 1
		return self.action

	def find_target_in_units(self, battle_units):
		target = None
		distance = WIDTH

		for enemy in battle_units:
			cur_distance = enemy.rect.x - self.rect.x
			if cur_distance < distance:
				if len(battle_units) <= 4:
					target = enemy
					distance = cur_distance
				elif len(battle_units) > 4 and enemy.attacking_me_shooters <= enemy.total_hp // self.damage:
					target = enemy
					distance = cur_distance

		return {'distance':distance, 'target':target}

	def find_target(self, battle_units, gf):
		target = None
		distance = WIDTH
		self.target_is_boss = False

		if gf.boss != None:
			if len(battle_units) > 0 and random.randint(1, 3) == 1:
				res = self.find_target_in_units(battle_units)
				target = res['target']
				distance = res['distance']
			else:
				target = gf.boss
				self.target_is_boss = True
		else:
			res = self.find_target_in_units(battle_units)
			target = res['target']
			distance = res['distance']

		if target != None and not self.target_is_boss:
			battle_units[battle_units.index(target)].attacking_me_shooters += 1
		self.target = target

	def stimpack(self, stimpack_speed):
		self.stimpack_speed = stimpack_speed
		self.on_stimpack = True
		if self.default_attack_speed - self.default_attack_speed * STIMPACK_BUFF != self.attack_speed:
			self.attack_speed -= self.attack_speed * STIMPACK_BUFF
			self.animation_speed -= self.animation_speed * STIMPACK_BUFF
		self.stimpack_iterations = 0
		self.stimpack_animation = True
		self.stimpack_animation_iterations = 0
		#print(f'stimpacked! attack - {self.attack_speed}; animation - {self.animation_speed}')

	def stop_stimpack(self):
		self.attack_speed = self.default_attack_speed
		self.animation_speed = self.default_animation_speed
		self.stimpack_iterations = 0
		self.on_stimpack = False
		self.stimpack_animation = True
		self.stimpack_animation_iterations = 0

	def new_level(self):
		self.level += 1
		self.damage = self.level * 5
		self.upgrade_cost = int(600 + (600*0.15)*self.level)
		#print(f'new level is - {self.level}')