import pygame, images, math
from datetime import datetime
from constants import *


class Castle:
	def __init__(self, level=1):
		self.castle_image = images.get_castle(skin='black')
		self.castle_rect = self.castle_image.get_rect()

		self.castle_rect.x = 100*OBJECT_MULTIPLYER_WIDTH
		self.castle_rect.y = HEIGHT - CASTLE_SIZE[1] - 80 * AVERAGE_MULTIPLYER

		self.rect = self.castle_rect

		self.level = level
		self.total_hp = 1500 + (self.level * 300)
		self.total_mana = 400 + (self.level * 100)

		self.hp = self.total_hp
		self.mana = self.total_mana

		self.mana_add_iterations = 0
		self.mana_add_iterations_slide = 0

		self.upgrade_cost = int(900 + (900*0.15)*self.level)

	async def new_level(self):
		self.level += 1
		self.total_hp = 1500 + (self.level * 300)
		self.total_mana = 400 + (self.level * 100)
		self.upgrade_cost = int(900 + (900*0.15)*self.level)

	async def update_hpbar_size(self, bar_size):
		Multiplyer = DEFAULT_HPBAR_SIZE[0] / self.total_hp
		return (math.ceil(DEFAULT_HPBAR_SIZE[0] - (self.total_hp - self.hp)*Multiplyer), bar_size[1])

	async def update_manabar_size(self, bar_size):
		Multiplyer = DEFAULT_MANABAR_SIZE[0] / self.total_mana
		return (math.ceil(DEFAULT_MANABAR_SIZE[0] - (self.total_mana - self.mana)*Multiplyer), bar_size[1])