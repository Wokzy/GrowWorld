import pygame, images, random, sys, set_config
from constants import *
from datetime import datetime
from scripts import Unit as unit
from scripts import objects


class GameFunctions:
	def __init__(self):
		self.in_battle = False
		self.battle_heroes = []
		self.battle_duration_left = None
		self.enemyes_amount = None
		self.enemy_line_time = FPS * random.randint(5, 10) / 10
		self.enemy_line_iteraion = 0
		self.wave = None

		self.additional_objects = []
		self.heroes = []

		self.enter_in_text_input = False
		self.text_input_obj = None
		self.text_input_index = None

		self.info_font = pygame.font.SysFont('Comic Sans MS', 15*AVERAGE_MULTIPLYER)
		self.wave = 1

	async def start_battle(self):
		self.enemyes_amount = self.wave * 30
		wave_speed = 30 + (self.wave // 100)
		self.in_battle = True
		row = 1

		if self.enemyes_amount > 6:
			for i in range(6):
				self.battle_heroes.append(unit.monster(self.wave, row))
				if row != 6:
					row += 1
				elif row == 6:
					row = 1
			self.enemy_line_iteraion = 0
			self.enemyes_amount -= 6

	async def update_battle(self, castle):
		if len(self.battle_heroes) == 0:
			await self.victory()
		elif castle.hp == 0:
			await self.defeat()

		for enemy in self.battle_heroes:
			update = enemy.update(castle)
			if update != None and update != ['Stay']:
				if update[0] == 'Attack':
					if castle.hp - update[1] >= 0:
						castle.hp -= update[1]
					else:
						castle.hp = 0
			if not enemy.alive:
				self.battle_heroes.remove(enemy)

		await self.add_line_with_enemyes()
		self.enemy_line_iteraion += 1

	async def add_line_with_enemyes(self):
		row = 1
		if self.enemyes_amount >= 6 and self.enemy_line_iteraion >= self.enemy_line_time:
			for i in range(6):
				self.battle_heroes.append(unit.monster(self.wave, row))
				if row != 6:
					row += 1
				elif row == 6:
					row = 1
			self.enemyes_amount -= 6
			self.enemy_line_iteraion = 0
			self.enemy_line_time = FPS * random.randint(5, 9) / 10
		elif self.enemyes_amount < 6  and self.enemy_line_iteraion >= self.enemy_line_time:
			for i in range(self.enemyes_amount):
				self.battle_heroes.append(unit.monster(self.wave, row))
				if row != 6:
					row += 1
				elif row == 6:
					row = 1
			self.enemyes_amount -= 6
			self.enemy_line_iteraion = 0
			self.enemy_line_time = FPS * random.randint(5, 9) / 10


	async def victory(self):
		print('VICTORY!!!')
		self.in_battle = False
		self.battle_heroes = []

	async def defeat(self):
		print('defeat')
		self.in_battle = False
		self.battle_heroes = []

	async def find_blitting_object(self):
		await self.update_settings_button()
		await self.update_attack_button()

		await self.update_settings_window()

	async def update_attack_button(self):
		flag = False
		obj_ = None
		for obj in self.additional_objects:
			if obj.name == 'attack_button':
				flag = True
				obj_ = obj
				break

		if not self.in_battle and not flag:
			self.additional_objects.insert(1, objects.Button('attack_button', images.get_fight_button(), (WIDTH - FIGHT_BUTTON_SIZE[0] - 5*OBJECT_MULTIPLYER_WIDTH, HEIGHT - FIGHT_BUTTON_SIZE[1] - 5*OBJECT_MULTIPLYER_HEIGHT)))
		elif self.in_battle and flag:
			self.additional_objects.remove(obj_)

	async def update_settings_button(self):
		flag = False
		obj_ = None
		for obj in self.additional_objects:
			if obj.name == 'settings_button':
				flag = True
				obj_ = obj
				break

		if not self.in_battle and not flag:
			self.additional_objects.insert(0, objects.Button('settings_button', images.get_settings_button(), (5*OBJECT_MULTIPLYER_WIDTH, 5*OBJECT_MULTIPLYER_HEIGHT)))
		elif self.in_battle and flag:
			self.additional_objects.remove(obj_)

	async def open_settings_window(self):
		window = objects.Window('settings_window', images.get_settings_window(), (WIDTH-SETTINGS_WINDOW_SIZE[0]-5*OBJECT_MULTIPLYER_WIDTH, 5*OBJECT_MULTIPLYER_HEIGHT))
		text_input_width = objects.TextInput('text_input_width', (100*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT), (window.rect.x + 50*OBJECT_MULTIPLYER_WIDTH, window.rect.y + 50*OBJECT_MULTIPLYER_HEIGHT), text=objects.Text('width_text', self.info_font.render(str(WIDTH), False, (0, 0, 0)), (window.rect.x + 50*OBJECT_MULTIPLYER_WIDTH, window.rect.y + 50*OBJECT_MULTIPLYER_HEIGHT), str(WIDTH)), type_='only_numbers')
		text_input_height = objects.TextInput('text_input_height', (100*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT), (window.rect.x + 50*OBJECT_MULTIPLYER_WIDTH, window.rect.y + 100*OBJECT_MULTIPLYER_HEIGHT), text=objects.Text('height_text', self.info_font.render(str(HEIGHT), False, (0, 0, 0)), (window.rect.x + 50*OBJECT_MULTIPLYER_WIDTH, window.rect.y + 100*OBJECT_MULTIPLYER_HEIGHT), str(HEIGHT)), type_='only_numbers')
		apply_settings_button = objects.Button('apply_settings_button', images.get_apply_settings_button(), (text_input_height.rect[0] - (12 * OBJECT_MULTIPLYER_WIDTH), text_input_height.rect[1] + APPLY_SETTIGS_BUTTON_SIZE[1] - (10 * OBJECT_MULTIPLYER_HEIGHT)))

		flag = False
		removing_list = []
		for obj in self.additional_objects:
			if obj.name == 'settings_window' or obj.name == 'text_input_width' or obj.name == 'text_input_height' or obj.name == 'apply_settings_button':
				obj.mode = False
				removing_list.append(obj)
				flag = True
		for obj in removing_list:
			self.additional_objects.remove(obj)
		if not flag:
			window.mode = True
			self.additional_objects.append(window)
			self.additional_objects.append(text_input_width)
			self.additional_objects.append(text_input_height)
			self.additional_objects.append(apply_settings_button)

	async def update_settings_window(self):
		if self.in_battle:
			removing_list = []
			for obj in self.additional_objects:
				if obj.name == 'settings_window' or obj.name == 'text_input_width' or obj.name == 'text_input_height' or obj.name == 'apply_settings_button':
					obj.mode = False
					removing_list.append(obj)
			for obj in removing_list:
				self.additional_objects.remove(obj)

	async def entering_in_text_input(self, event):
		if event.key == pygame.K_BACKSPACE and self.text_input_obj.text.text != '':
			self.text_input_obj.text.text = self.text_input_obj.text.text[::-1][1::][::-1]
		elif event.key == pygame.K_SPACE:
			self.text_input_obj.text.text = self.text_input_obj.text.text + ' '
		elif event.key != pygame.K_BACKSPACE:
			if self.text_input_obj.type_ == 'only_numbers':
				if event.key in NUMBERS_KEYS:
					self.text_input_obj.text.text += event.unicode
			else:
				self.text_input_obj.text.text += event.unicode
		self.text_input_obj.text.image = self.info_font.render(self.text_input_obj.text.text, False, (0, 0, 0))
		self.additional_objects[await self.text_input_obj.find_index(self)].text = self.text_input_obj.text

	async def apply_settings(self):
		width = None
		height = None
		for obj in self.additional_objects:
			if obj.name == 'text_input_width':
				width = int(obj.text.text)
			elif obj.name == 'text_input_height':
				height = int(obj.text.text)
			if width != None and height != None:
				break

		set_config.set_config(width=width, height=height)
		pygame.quit()
		sys.exit()