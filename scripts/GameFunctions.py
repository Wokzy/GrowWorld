import pygame, images, random
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
		self.enemy_line_time = random.randint(5, 10) / 10
		self.enemy_line_timer = None
		self.wave = None

		self.additional_objects = []

		self.enter_in_text_input = False
		self.text_input_obj = None
		self.text_input_index = None

		self.info_font = pygame.font.SysFont('Comic Sans MS', INFO_FONT_SIZE)

	async def start_battle(self, wave):
		self.enemyes_amount = wave * 30
		wave_speed = 30 + (wave // 100)
		self.in_battle = True
		self.wave = wave
		row = 1

		if self.enemyes_amount > 6:
			for i in range(6):
				self.battle_heroes.append(unit.monster(wave, row))
				if row != 6:
					row += 1
				elif row == 6:
					row = 1
			self.enemy_line_timer = datetime.now()
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

	async def add_line_with_enemyes(self):
		row = 1
		if self.enemyes_amount >= 6 and (datetime.now() - self.enemy_line_timer).total_seconds() >= self.enemy_line_time:
			for i in range(6):
				self.battle_heroes.append(unit.monster(self.wave, row))
				if row != 6:
					row += 1
				elif row == 6:
					row = 1
			self.enemyes_amount -= 6
			self.enemy_line_timer = datetime.now()
			self.enemy_line_time = random.randint(5, 9) / 10
		elif self.enemyes_amount < 6  and (datetime.now() - self.enemy_line_timer).total_seconds() >= self.enemy_line_time:
			for i in range(self.enemyes_amount):
				self.battle_heroes.append(unit.monster(self.wave, row))
				if row != 6:
					row += 1
				elif row == 6:
					row = 1
			self.enemyes_amount -= 6
			self.enemy_line_timer = datetime.now()
			self.enemy_line_time = random.randint(5, 9) / 10


	async def victory(self):
		print('VICTORY!!!')
		self.in_battle = False
		self.battle_heroes = []

	async def defeat(self):
		print('defeat')
		self.in_battle = False
		self.battle_heroes = []

	async def find_blitting_object(self):
		if not self.in_battle and not objects.Button('settings_button', images.get_settings_button(), (5*OBJECT_MULTIPLYER_WIDTH, 5*OBJECT_MULTIPLYER_HEIGHT)) in self.additional_objects:
			self.additional_objects.insert(0, objects.Button('settings_button', images.get_settings_button(), (5*OBJECT_MULTIPLYER_WIDTH, 5*OBJECT_MULTIPLYER_HEIGHT)))

		await self.update_settings_window()

	async def open_settings_window(self):
		window = objects.Window('settings_window', images.get_settings_window(), (WIDTH-SETTINGS_WINDOW_SIZE[0]-5*OBJECT_MULTIPLYER_WIDTH, 5*OBJECT_MULTIPLYER_HEIGHT))
		text_input_width = objects.TextInput('text_input_width', (100*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT), (window.rect.x + 50*OBJECT_MULTIPLYER_WIDTH, window.rect.y + 50*OBJECT_MULTIPLYER_HEIGHT), text=objects.Text('width_text', self.info_font.render(str(WIDTH), False, (0, 0, 0)), (window.rect.x + 50*OBJECT_MULTIPLYER_WIDTH, window.rect.y + 50*OBJECT_MULTIPLYER_HEIGHT), str(WIDTH)))
		text_input_height = objects.TextInput('text_input_height', (100*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT), (window.rect.x + 50*OBJECT_MULTIPLYER_WIDTH, window.rect.y + 100*OBJECT_MULTIPLYER_HEIGHT), text=objects.Text('height_text', self.info_font.render(str(HEIGHT), False, (0, 0, 0)), (window.rect.x + 50*OBJECT_MULTIPLYER_WIDTH, window.rect.y + 100*OBJECT_MULTIPLYER_HEIGHT), str(HEIGHT)))

		flag = False
		removing_list = []
		for obj in self.additional_objects:
			if obj.name == 'settings_window' or obj.name == 'text_input_width' or obj.name == 'text_input_height':
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

	async def update_settings_window(self):
		if self.in_battle:
			removing_list = []
			for obj in self.additional_objects:
				if obj.name == 'settings_window' or obj.name == 'text_input_width' or obj.name == 'text_input_height':
					obj.mode = False
					removing_list.append(obj)
			for obj in removing_list:
				self.additional_objects.remove(obj)