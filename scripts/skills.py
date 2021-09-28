import images
from constants import *


class BonusGold:
	def __init__(self, level):
		self.name = self.__class__.__name__
		self.image = images.get_bonus_gold_skill_button()
		self.level = level
		self.max_level = 20

		self.bonus_percent = 2.5*self.level
		self.upgrade_gold_cost = 400 + 350*self.level
		self.upgrade_crystals_cost = 5

		self.description = f'Gives additional \n gold bonus \n {self.bonus_percent}%'

	def upgrade(self, gf):
		if gf.gold >= self.upgrade_gold_cost and gf.crystal >= self.upgrade_crystals_cost and self.level+1 <= self.max_level:
			gf.gold -= self.upgrade_gold_cost
			gf.crystal -= self.upgrade_crystals_cost
			self.__init__(self.level+1)
			gf.update_bonus_gold()
		elif self.level+1 > self.max_level:
			print('reached max level!')
		else: print('not enough payment')

	def refresh(self, gf):
		pass


class CriticalShot:
	def __init__(self, level):
		self.name = self.__class__.__name__
		self.image = images.get_critical_shot_skill_button()
		self.level = level
		self.max_level = 10

		self.chance = 5*self.level
		self.upgrade_gold_cost = 600 + 500*self.level
		self.upgrade_crystals_cost = 4 + self.level

		self.description = f"With chance \n{self.chance}% town shooter's \n damage will be equal \n 225%"

	def upgrade(self, gf):
		if gf.gold >= self.upgrade_gold_cost and gf.crystal >= self.upgrade_crystals_cost and self.level+1 <= self.max_level:
			gf.gold -= self.upgrade_gold_cost
			gf.crystal -= self.upgrade_crystals_cost
			self.__init__(self.level+1)
		elif self.level+1 > self.max_level:
			print('reached max level!')
		else: print('not enough payment')