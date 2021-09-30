import pygame, images, random, math
from constants import *
from datetime import datetime


class ToxicBullet:
	def __init__(self, damage, position, target, speed=15):
		self.images = images.get_toxic_bullet()
		self.image = self.images[0]
		self.damage = damage
		self.speed = speed*AVERAGE_MULTIPLYER
		self.target = target

		self.rect = self.image.get_rect()
		self.rect.center = position

		self.alive = True

		self.animation_speed = FPS // 3
		self.animation_iteration = 0

	def update(self):
		self.rect.x -= self.speed

		if self.animation_iteration >= self.animation_speed:
			if self.images.index(self.image) +1 != len(self.images):
				self.image = self.images[self.images.index(self.image) + 1]
			else: self.image = self.images[0]
			self.animation_iteration = 0

		self.animation_iteration += 1




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
			#print(self.cost + ((self.cost // 100) * gf.bonus_gold))
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






class RangeEnemy:
	def __init__(self, type_surface, hp, speed, damage, attack_speed, imgs, size, wave, row_position=1, attack_range=60):
		self.type_surface = type_surface # Ground / Air
		self.type_damage = 'Range' # Range / Melee
		self.total_hp = hp
		self.speed = speed # Speed of unit in pixels
		self.damage = damage # Damage in points
		self.attack_speed = attack_speed # Attack speed in iterations
		self.images = imgs
		self.image = self.images['stay_image']
		self.attack_image = self.images['attack_image']
		self.rect = self.image.get_rect()
		self.size = size
		self.row_position = row_position # 1 - 6 position
		self.attack_range = attack_range*OBJECT_MULTIPLYER_WIDTH # Espessially for 'Range' units

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

		self.mode = 'stay'

		self.animation_move_speed = FPS*0.4
		self.animation_attack_speed = self.attack_speed*0.8

		self.animation_attack_iteration = 0
		self.animation_move_iteration = 0

	def update(self, castle, gf):
		if self.mode == 'stay' and self.image != self.images['stay_image']:
			self.image = self.images['stay_image']
			self.animation_move_iteration = 0
		elif self.mode == 'attack' and self.image != self.attack_image:
			self.image = self.attack_image
		elif self.mode == 'move' and self.image not in self.images['move_images']:
			self.image = self.images['move_images'][0]
		elif self.mode == 'move' and self.animation_move_iteration >= self.animation_move_speed:
			if self.images['move_images'].index(self.image) + 1 != len(self.images['move_images']):
				self.image = self.images['move_images'][self.images['move_images'].index(self.image) + 1]
			else:
				self.image = self.images['move_images'][0]
			self.animation_move_iteration = 0

		if self.animation_attack_iteration >= self.animation_attack_speed:
			self.animation_attack_iteration = 0
			self.mode = 'stay'

		if self.mode == 'move':
			self.animation_move_iteration += 1
		elif self.mode == 'attack':
			self.animation_attack_iteration += 1



		self.attack_iteration += 1
		if self.target != None and self.target.hp <= 0:
			self.target = None
		if self.target == None:
			self.find_target(gf)
		if self.hp <= 0:
			self.alive = False
			gf.gold += self.cost + ((self.cost // 100) * gf.bonus_gold)
			#print(self.cost + ((self.cost // 100) * gf.bonus_gold))
			return None
		if self.rect.x > self.target.rect.x + self.attack_range:
			self.rect.x -= self.speed
			self.mode = 'move'
		elif self.rect.x <= self.target.rect.x + self.attack_range:
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
			self.mode = 'attack'
			self.attack_iteration = 0
			return ['ToxicBullet', self.damage, (self.rect.x, self.rect.y + self.size[1] // 2), self.target]
		else:
			return ['Stay']

	def bite(self, dmg):
		self.hp -= dmg

	def find_target(self, gf):
		if len(gf.allies_units) > 0:
			while self.target == None or self.target != gf.castle and self.target.type_surface == 'Boom':
				self.target = random.choice([gf.castle, random.choice(gf.allies_units)])
				while self.target.__class__.__name__ == 'RocketBoom':
					self.target = random.choice([gf.castle, random.choice(gf.allies_units)])
		else: self.target = gf.castle

"""
class Boss:
	def __init__(self, name, hp, speed, damage, attack_speed, imgs, size):
		pass
"""


def monster(wave, row_position):
	return Enemy('Ground', 'Melee', ((wave//3)+1)*250, random.randint(2, 4)*AVERAGE_MULTIPLYER, 15, FPS*0.4, images.get_monster(), MONSTER_SIZE, wave, row_position=row_position)

def range_monster(wave, row_position):
	return RangeEnemy('Ground', ((wave//3)+1)*200, random.randint(1, 3)*AVERAGE_MULTIPLYER, 10, FPS, images.get_range_monster(), RANGE_MONSTER_SIZE, wave, row_position=row_position, attack_range=random.randint(250, 400))