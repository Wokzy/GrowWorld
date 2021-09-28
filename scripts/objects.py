import pygame, images
from constants import *
from scripts import heroes, skills


class Button:
	def __init__(self, name, image, position):
		self.name = name
		self.image = image

		self.rect = image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

	async def action(self, gf):
		if self.name == 'settings_button':
			await gf.open_settings_window()
		elif self.name == 'apply_settings_button':
			await gf.apply_settings()
		elif self.name == 'attack_button':
			await gf.start_battle()
		elif self.name == 'close_button':
			await gf.close_everything()
		elif self.name == 'equip':
			idx = 23123123123123
			for i in range(len(gf.heroes)):
				if gf.heroes[i].name == gf.upgrading_hero_obj.name:
					idx = i
					break
			if idx != 23123123123123:
				pos = gf.heroes[idx].tower_position
				gf.heroes[idx] = heroes.Nothing(pos, gf)
			gf.upgrading_hero_obj.tower_position = gf.heroes[gf.heroes.index(gf.changing_unit_noun)].tower_position
			gf.upgrading_hero_obj.init(gf)
			gf.heroes[gf.heroes.index(gf.changing_unit_noun)] = gf.upgrading_hero_obj
			await gf.save_state()
			await gf.close_everything()
		elif self.name == 'take_off':
			gf.heroes[gf.heroes.index(gf.changing_unit_noun)] = heroes.Nothing(gf.heroes[gf.heroes.index(gf.changing_unit_noun)].tower_position, gf)
			await gf.save_state()
			await gf.close_everything()
		elif self.name == 'Upgrade_hero':
			gf.upgrade_hero_action()
			await gf.save_state()
		elif self.name == 'goto_town':
			await gf.goto_town()
		elif self.name == 'goto_castle':
			await gf.goto_castle()
		elif self.name == 'buy_crystal':
			gf.buy_crystal()
		elif self.name == 'sell_crystal':
			gf.sell_crystal()
		elif self.name == 'remove_data':
			await gf.afford_removing_data()
		elif self.name == 'afford_removing_data_button':
			gf.remove_data()
		elif self.name == 'not_afford_removing_data_button':
			gf.close_settings_window()
		elif self.name == 'skills_button':
			await gf.open_skills_window()
		elif self.name == 'bonus_gold_skill_button':
			await gf.upgrade_skill(skills.BonusGold(0))
		elif self.name == 'critical_shot_skill_button':
			await gf.upgrade_skill(skills.CriticalShot(0))
		elif self.name == 'Upgrade_skill':
			gf.upgrading_skill.upgrade(gf)
			if gf.upgrading_skill.name not in [i.name for i in gf.skills]:
				gf.skills.append(gf.upgrading_skill)
			skill = gf.upgrading_skill
			await gf.close_everything()
			await gf.open_skills_window()
			await gf.upgrade_skill(skill)
			await gf.save_state()


class Window:
	def __init__(self, name, image, position):
		self.name = name
		self.image = image

		self.rect = image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

		self.mode = False # True or False (hide or show)

	async def action(self, gf):
		#print('aboba')
		if 'changing_hero' in self.name:
			gf.upgrade_hero(int(self.name.split(' ')[1]))

class TextInput:
	def __init__(self, name, size, position, text='', type_='default'):
		self.name = name
		self.image = images.get_text_input(size)

		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

		self.mode = False
		self.text = text

		self.type_ = type_ # Type - only numbers/default

	async def action(self, gf):
		pass

	async def find_index(self, gf):
		for obj in range(len(gf.additional_objects)):
			if gf.additional_objects[obj].name == gf.text_input_obj.name:
				return obj

class Text:
	def __init__(self, name, image, position, text=''):
		self.name = name
		self.image = image
		self.rect = position
		self.text = text

class UpgradeShooterButton:
	def __init__(self, position):
		self.name = 'upgrade_shooters_button'
		self.image = images.get_upgrade_shooter_button_image()

		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

	async def action(self, gf):
		if gf.gold - gf.town_shooters[0].upgrade_cost >= 0:
			gf.gold -= gf.town_shooters[0].upgrade_cost
			for town_shooter in gf.town_shooters:
				town_shooter.new_level()
			await gf.save_state()
		else: print('not enought gold')

class UpgradeCastleButton:
	def __init__(self, position):
		self.name = 'upgrade_castle_button'
		self.image = images.get_upgrade_shooter_button_image()

		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

	async def action(self, gf):
		if gf.gold - gf.castle.upgrade_cost >= 0:
			gf.gold -= gf.castle.upgrade_cost
			await gf.castle.new_level()
			await gf.save_state()
		else: print('not enought gold')

class Image:
	def __init__(self, image, position, name=''):
		self.name = name
		self.image = image

		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

	async def action(self, gf):
		pass