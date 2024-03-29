import pygame, images, random, sys, set_config, pickle, math, os, time
from constants import *
from datetime import datetime
from scripts import Enemy as enemy
from scripts import Enemy as ENEMY
from scripts import objects, heroes, castle, Town_shooters, GroundObjects, skills
from scripts import Boss as boss


class GameFunctions:
	def __init__(self):
		self.in_battle = False
		self.battle_heroes = []
		self.allies_units = []
		self.total_heroes = []
		self.skills = []

		self.special_buttons = {'goto_town':objects.Button('goto_town', images.get_goto_town_button(), (20*OBJECT_MULTIPLYER_WIDTH, 45*OBJECT_MULTIPLYER_HEIGHT)), 'goto_castle':objects.Button('goto_castle', images.get_goto_castle_button(), (WIDTH - 20*OBJECT_MULTIPLYER_WIDTH - MOVE_GLOBAL_LOCATION_BUTTON_SIZE[0], 45*OBJECT_MULTIPLYER_HEIGHT))}
		self.special_buttons_avalible = True

		self.battle_duration_left = None
		self.enemyes_amount = None
		self.enemy_line_time = FPS * random.randint(50, 90) / 100
		self.enemy_line_iteraion = 0
		self.wave = 1

		self.data = False
		try:
			self.data = self.load_state()
		except Exception as e: print(e)

		if self.data:
			for skill in self.data['skills']:
				if skill['name'] == 'BonusGold':
					self.skills.append(skills.BonusGold(skill['level']))
				elif skill['name'] == 'CriticalShot':
					self.skills.append(skills.CriticalShot(skill['level']))
			self.castle = castle.Castle(self.data['castle_info']['level'])
			self.wave = self.data['wave']
			try: 
				self.gold = self.data['gold']
				self.crystal = self.data['crystal']
			except Exception as e:
				print(e)
				self.gold = 0
				self.crystal = 0
			self.heroes = []
			self.total_heroes = []
			#self.heroes = [heroes.StimManager(1, 1, self), heroes.Maradauer(1, 2, self)]
			for hero in self.data['heroes_info']:
				if hero['name'] == 'StimManager':
					self.heroes.append(heroes.StimManager(hero['level'], hero['tower_position'], self))
				elif hero['name'] == 'Maradauer':
					self.heroes.append(heroes.Maradauer(hero['level'], hero['tower_position'], self))
				elif hero['name'] == 'Nothing':
					self.heroes.append(heroes.Nothing(hero['tower_position'], self))
				elif hero['name'] == 'UnitHealer':
					self.heroes.append(heroes.UnitHealer(hero['level'], hero['tower_position'], self))
				elif hero['name'] == 'RocketMan':
					self.heroes.append(heroes.RocketMan(hero['level'], hero['tower_position'], self))
				else: print(hero['name'])
			self.town_shooters = []
			for i in range(4):
				for g in range(5):
					self.town_shooters.append(Town_shooters.TownShooter(self.data['town_shooters_info'][i+g]['level'], images.get_town_shooter(), g, i))
			for hero in self.data['total_heroes_info']:
				if hero['name'] == 'StimManager':
					self.total_heroes.append(heroes.StimManager(hero['level'], hero['tower_position'], self))
				elif hero['name'] == 'Maradauer':
					self.total_heroes.append(heroes.Maradauer(hero['level'], hero['tower_position'], self))
				elif hero['name'] == 'UnitHealer':
					self.total_heroes.append(heroes.UnitHealer(hero['level'], hero['tower_position'], self))
				elif hero['name'] == 'RocketMan':
					self.total_heroes.append(heroes.RocketMan(hero['level'], hero['tower_position'], self))
				else: print(hero['name'])
		else:
			self.castle = castle.Castle()
			self.total_heroes = [heroes.StimManager(1, 1, self), heroes.Maradauer(1, 2, self), heroes.UnitHealer(1, 3, self), heroes.RocketMan(1, 4, self)]
			self.heroes = [heroes.Nothing(1, self), heroes.Nothing(2, self), heroes.Nothing(3, self), heroes.Nothing(4, self)]
			self.town_shooters = []
			self.gold = 0
			self.crystal = 0
			self.skills = []

		self.additional_objects = []
		self.battle_objects = []
		self.info_objects = []
		self.prev_additional_objects = []
		self.targetting_prev_additional_objects = []

		self.wave_bar_position = (WIDTH-WAVE_BAR_BACKGROUND_SIZE[0], DEFAULT_MANABAR_SIZE[1]+WAVE_BAR_BACKGROUND_SIZE[1])
		self.wave_bar = objects.Window('wave_bar', images.get_white_window(WAVE_BAR_BACKGROUND_SIZE), self.wave_bar_position)
		self.default_wave_bar = self.wave_bar
		self.wave_bar_background = objects.Window('wave_bar_background', images.get_gray_window(WAVE_BAR_BACKGROUND_SIZE), self.wave_bar_position)

		self.enter_in_text_input = False
		self.text_input_obj = None
		self.text_input_index = None

		self.info_font = pygame.font.SysFont('Comic Sans MS', 15*AVERAGE_MULTIPLYER)
		self.info_font_big = pygame.font.SysFont('Comic Sans MS', 25*AVERAGE_MULTIPLYER)
		self.info_font_small = pygame.font.SysFont('Comic Sans MS', 10*AVERAGE_MULTIPLYER)
		self.wave_font = pygame.font.SysFont('AA Higherup', WAVE_BAR_BACKGROUND_SIZE[1])

		self.init_optimization()

		self.changing_unit_verb = False
		self.upgrading_hero = False
		self.upgrading_hero_obj = None

		self.hero_target_position = ()
		self.targetting = False
		self.targetting_hero = None

		self.global_location = 'Castle' # Castle or Town
		self.cost_of_crystal = ((self.wave//10)+1) * 100 + 15*self.wave + 500
		self.trading = False

		self.on_stats_traiding_obj = None

		self.bonus_gold = 0 # In percent
		self.active_bonuses = []

		self.update_bonus_gold()

		self.boss = None
		self.boss_already_went = False

	async def start_battle(self):
		self.battle_objects = []
		print(f'wave - {self.wave}')
		self.enemyes_amount = (self.wave // 3 + 1) * 40
		self.max_enemyes = self.enemyes_amount
		wave_speed = 30 + (self.wave // 100)
		self.in_battle = True
		row = 1

		if self.enemyes_amount > 6:
			for i in range(6):
				self.battle_heroes.append(enemy.monster(self.wave, row))
				if row != 6:
					row += 1
				elif row == 6:
					row = 1
			self.enemy_line_iteraion = 0
			self.enemyes_amount -= 6

		self.wave_text = (objects.Text('wave_text', self.wave_font.render(str(f'Wave - {self.wave}'), False, (0, 0, 0)), (self.wave_bar_position[0]+3*AVERAGE_MULTIPLYER, self.wave_bar_position[1]+2*AVERAGE_MULTIPLYER), str(f'Wave - {self.wave}')))
		self.boss = None
		self.boss_already_went = False

		self.wave_bar = objects.Window('wave_bar', images.get_white_window(WAVE_BAR_BACKGROUND_SIZE), self.wave_bar_position)


	def end_battle(self):
		self.battle_objects = []
		self.allies_units = []

		for hero in self.heroes:
			hero.attacking = False
		for shooter in self.town_shooters:
			shooter.target = None

		self.wave_bar = self.default_wave_bar
		self.boss = None
		self.boss_already_went = False

	async def update_battle(self):
		if len(self.battle_heroes) == 0 and self.enemyes_amount == 0 and self.boss == None:
			self.end_battle()
			await self.victory()
		elif self.castle.hp <= 0:
			self.end_battle()
			await self.defeat()

		if self.enemyes_amount <= 5 and self.boss == None and self.boss_already_went == False and self.wave % 5 == 0:
			self.boss = random.choice([boss.RedGiant(self.wave//15)])
			self.boss_already_went = True

		if self.boss != None:
			if self.boss.hp <= 0:
				self.boss = None

		for enemy in self.battle_heroes:
			update = enemy.update(self.castle, self)
			if update != None and update != ['Stay']:
				if update[0] == 'Attack':
					if enemy.target.hp - update[1] >= 0:
						enemy.target.hp -= update[1]
					else:
						enemy.target.hp = 0
				elif update[0] == 'ToxicBullet':
					self.battle_objects.append(ENEMY.ToxicBullet(update[1], update[2], update[3]))
			if not enemy.alive:
				self.battle_heroes.remove(enemy)

		if self.boss == None:
			self.wave_bar.image = pygame.transform.scale(self.wave_bar.image, (int(WAVE_BAR_BACKGROUND_SIZE[0]*(self.enemyes_amount / self.max_enemyes)), WAVE_BAR_BACKGROUND_SIZE[1]))
		else:
			self.wave_bar.image = pygame.transform.scale(images.get_red_bar(), (int(WAVE_BAR_BACKGROUND_SIZE[0]*(self.boss.hp / self.boss.max_hp)), WAVE_BAR_BACKGROUND_SIZE[1]))
			self.wave_text = (objects.Text('wave_text', self.wave_font.render(str(f'{self.boss.hp}'), False, (0, 0, 0)), (self.wave_bar_position[0]+3*AVERAGE_MULTIPLYER, self.wave_bar_position[1]+2*AVERAGE_MULTIPLYER), str(f'{self.boss.hp}')))



		for obj in self.battle_objects:
			obj.update()
			if obj.__class__.__name__ == 'ToxicBullet':
				if obj.rect.colliderect(obj.target):
					if obj.target.hp - obj.damage >= 0:
						obj.target.hp -= obj.damage
					else:
						obj.target.hp = 0
					self.battle_objects.remove(obj)
					continue
				elif obj.rect.colliderect(self.castle):
					if self.castle.hp - obj.damage >= 0:
						self.castle.hp -= obj.damage
					else:
						self.castle.hp = 0
					self.battle_objects.remove(obj)
					continue

		await self.add_line_with_enemyes()
		self.enemy_line_iteraion += 1

	async def add_line_with_enemyes(self):
		row = 1
		if self.enemyes_amount >= 6 and self.enemy_line_iteraion >= self.enemy_line_time:
			for i in range(2):
				self.battle_heroes.append(enemy.monster(self.wave, row))
				self.battle_heroes.append(enemy.monster(self.wave, row))
				self.battle_heroes.append(enemy.range_monster(self.wave, row))
				if row != 6:
					row += 1
				elif row == 6:
					row = 1
			self.enemyes_amount -= 6
			self.enemy_line_iteraion = 0
			self.enemy_line_time = FPS * random.randint(50, 90) / 100
		elif self.enemyes_amount < 6  and self.enemy_line_iteraion >= self.enemy_line_time:
			for i in range(self.enemyes_amount):
				self.battle_heroes.append(enemy.monster(self.wave, row))
				if row != 6:
					row += 1
				elif row == 6:
					row = 1
			self.enemyes_amount = 0
			self.enemy_line_iteraion = 0
			self.enemy_line_time = FPS * random.randint(50, 90) / 100


	async def victory(self):
		print('VICTORY!!!')
		self.in_battle = False
		self.battle_heroes = []
		self.allies_units = []
		self.wave += 1
		self.crystal += 1
		await self.save_state()
		for obj in self.additional_objects:
			if obj.name == 'wave_text': self.additional_objects.remove(obj)

	async def defeat(self):
		print(f'defeat - {len(self.battle_heroes)}')
		self.in_battle = False
		self.battle_heroes = []
		self.allies_units = []
		await self.save_state()
		for obj in self.additional_objects:
			if obj.name == 'wave_text': self.additional_objects.remove(obj)

	async def find_blitting_object(self):
		if self.global_location == 'Castle':
			await self.update_attack_button()
		await self.update_settings_button()

		await self.update_settings_window()
		await self.update_upgrading()
		await self.update_skills_button()

		if self.upgrading_hero:
			await self.update_upgrading_hero()

		if self.trading: await self.update_trading()
		if self.targetting: self.update_targetting()

	def init_optimization(self):
		self.attack_button_on = False
		self.settings_window_on = False
		self.settings_button_on = False
		self.upgrading_window_on = False
		self.skills_button_on = False
		self.skills_window_on = False
		self.upgrading_skill_flag = False

	async def update_attack_button(self):
		if self.in_battle and self.attack_button_on and self.prev_additional_objects == []:
			obj_ = None
			for obj in self.additional_objects:
				if obj.name == 'attack_button':
					obj_ = obj
					break
			self.additional_objects.remove(obj_)
			self.attack_button_on = False
		elif not self.in_battle and not self.attack_button_on and self.prev_additional_objects == []:
			for obj in self.additional_objects:
				if obj.name == 'attack_button':
					break
			self.additional_objects.insert(1, objects.Button('attack_button', images.get_fight_button(), (WIDTH - FIGHT_BUTTON_SIZE[0] - 5*OBJECT_MULTIPLYER_WIDTH, HEIGHT - FIGHT_BUTTON_SIZE[1] - 5*OBJECT_MULTIPLYER_HEIGHT)))
			self.attack_button_on = True

	async def update_settings_button(self):
		if self.prev_additional_objects == [] or self.additional_objects == [objects.Button('settings_button', images.get_settings_button(), (5*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT))]:
			if not self.in_battle and not self.settings_button_on:
				for obj in self.additional_objects:
					if obj.name == 'settings_button':
						break
				self.additional_objects.insert(0, objects.Button('settings_button', images.get_settings_button(), (5*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT)))
				self.settings_button_on = True
			elif self.in_battle and self.settings_button_on:
				obj_ = None
				for obj in self.additional_objects:
					if obj.name == 'settings_button':
						obj_ = obj
						break
				self.additional_objects.remove(obj_)
				self.settings_button_on = False

	async def open_settings_window(self):
		window = objects.Window('settings_window', images.get_settings_window(), (WIDTH-SETTINGS_WINDOW_SIZE[0]-5*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT))
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
			self.prev_additional_objects = list(self.additional_objects)
			self.additional_objects = [objects.Button('settings_button', images.get_settings_button(), (5*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT))]
			self.additional_objects.append(window)
			self.additional_objects.append(text_input_width)
			self.additional_objects.append(text_input_height)
			self.additional_objects.append(apply_settings_button)
			self.additional_objects.append(objects.Button('remove_data', images.get_remove_data(), (WIDTH-SETTINGS_WINDOW_SIZE[0]+10*OBJECT_MULTIPLYER_WIDTH, apply_settings_button.rect.y + 50*OBJECT_MULTIPLYER_HEIGHT)))
			self.settings_window_on = True
		else:
			self.close_settings_window()

	def close_settings_window(self):
		self.additional_objects = list(self.prev_additional_objects)
		self.prev_additional_objects = []
		self.settings_window_on = False

	async def update_settings_window(self):
		if self.in_battle and self.settings_window_on:
			removing_list = []
			for obj in self.additional_objects:
				if obj.name == 'settings_window' or obj.name == 'text_input_width' or obj.name == 'text_input_height' or obj.name == 'apply_settings_button':
					obj.mode = False
					removing_list.append(obj)
			for obj in removing_list:
				self.additional_objects.remove(obj)
			self.settings_window_on = False

	async def entering_in_text_input(self, event):
		if event.key == pygame.K_BACKSPACE and self.text_input_obj.text.text != '':
			self.text_input_obj.text.text = self.text_input_obj.text.text[::-1][1::][::-1]
		elif event.key == pygame.K_SPACE:
			self.text_input_obj.text.text = self.text_input_obj.text.text + ' '
		elif event.key != pygame.K_BACKSPACE:
			if self.text_input_obj.type_ == 'only_numbers':
				if event.unicode in NUMBERS_KEYS:
					self.text_input_obj.text.text += event.unicode
			else:
				self.text_input_obj.text.text += event.unicode
		self.text_input_obj.text.image = self.info_font.render(self.text_input_obj.text.text, False, (0, 0, 0))
		self.additional_objects[await self.text_input_obj.find_index(self)].text = self.text_input_obj.text

	async def afford_removing_data(self):
		window_size = (500, 250)
		window_position = (WIDTH//2 - window_size[0]//2, HEIGHT//2 - window_size[1]//2)
		self.additional_objects = [objects.Window('afford_removing_data_window', images.get_gray_window(window_size), window_position)]

		warning_text = 'WARNING!!!'
		description_text = 'This function removes all your saved data'
		description_text_2 = 'Progress, gold, crystals, upgrades, waves etc.'
		sure_text = 'ARE YOU SURE IN REMOVING DATA?'

		self.additional_objects.append(objects.Text('warning_text', self.info_font_big.render(warning_text, False, (255, 0, 0)), (window_position[0]-50*OBJECT_MULTIPLYER_WIDTH + window_size[0]//2, window_position[1] + 10*OBJECT_MULTIPLYER_HEIGHT)))
		self.additional_objects.append(objects.Text('description_text', self.info_font.render(description_text, False, (255, 255, 255)), (window_position[0]+70*OBJECT_MULTIPLYER_WIDTH, window_position[1] + 40*OBJECT_MULTIPLYER_HEIGHT)))
		self.additional_objects.append(objects.Text('description_text_2', self.info_font.render(description_text_2, False, (255, 255, 255)), (window_position[0]+70*OBJECT_MULTIPLYER_WIDTH, window_position[1] + 70*OBJECT_MULTIPLYER_HEIGHT)))
		self.additional_objects.append(objects.Text('sure_text', self.info_font.render(sure_text, False, (255, 255, 255)), (window_position[0]+70*OBJECT_MULTIPLYER_WIDTH, window_position[1] + 100*OBJECT_MULTIPLYER_HEIGHT)))
		self.additional_objects.append(objects.Button('afford_removing_data_button', images.get_yes_button(), (window_position[0] + 40*OBJECT_MULTIPLYER_WIDTH, window_position[1] + window_size[1] - 5*OBJECT_MULTIPLYER_HEIGHT - YES_BUTTON_SIZE[1])))
		self.additional_objects.append(objects.Button('not_afford_removing_data_button', images.get_no_button(), (window_position[0] + window_size[0] - NO_BUTTON_SIZE[0] - 40*OBJECT_MULTIPLYER_WIDTH, window_position[1] + window_size[1] - 5*OBJECT_MULTIPLYER_HEIGHT - NO_BUTTON_SIZE[1])))

	def remove_data(self):
		os.remove('save.bin')
		print('REMOVED ALL USER DATA!')
		#time.sleep(5)
		pygame.quit()
		sys.exit()


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

	async def save_state(self):
		castle_info = {'level': self.castle.level}
		town_shooters_info = []
		heroes_info = []
		total_heroes_info = []

		for town_shooter in self.town_shooters:
			town_shooters_info.append({'level': town_shooter.level})

		for hero in self.heroes:
			if hero.__class__.__name__ != 'Nothing':
				heroes_info.append({'name':hero.__class__.__name__, 'level':hero.level, 'tower_position':hero.tower_position})
			else:
				heroes_info.append({'name':hero.__class__.__name__, 'tower_position':hero.tower_position})
		for hero in self.total_heroes:
			total_heroes_info.append({'name':hero.__class__.__name__, 'level':hero.level, 'tower_position':hero.tower_position})

		with open('save.bin', 'wb') as f:
			pickle.dump({'castle_info':castle_info,
						'town_shooters_info':town_shooters_info,
						'heroes_info':heroes_info,
						'wave':self.wave,
						'gold':self.gold,
						'crystal':self.crystal,
						'total_heroes_info':total_heroes_info,
						'skills':[{'name':skill.name, 'level':skill.level} for skill in self.skills]}, f)
			f.close()

	def load_state(self):
		data = None

		with open('save.bin', 'rb') as f:
			data = pickle.load(f)

		return data

	def init_objects(self):
		self.info_objects.append(objects.Window('gold_window', images.get_text_background((100*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT)), (0, 0)))
		self.info_objects.append(objects.Window('crystal_window', images.get_text_background((100*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT)), ((100+15)*OBJECT_MULTIPLYER_WIDTH, 0)))
		self.info_objects.append(objects.Text('gold_text', self.info_font.render(str(self.gold), False, (240, 236, 55)), (0, 0)))
		self.info_objects.append(objects.Image(images.get_crystal((15*OBJECT_MULTIPLYER_WIDTH, 15*OBJECT_MULTIPLYER_HEIGHT)), ((115+2)*OBJECT_MULTIPLYER_WIDTH, 0)))
		self.info_objects.append(objects.Text('crystal_text', self.info_font.render(str(self.crystal), False, (25, 210, 25)), ((115+20)*OBJECT_MULTIPLYER_WIDTH, 0)))

	async def update_upgrading(self):
		if self.prev_additional_objects == []:
			if not self.in_battle:
				window_size = (150*OBJECT_MULTIPLYER_WIDTH, 150*OBJECT_MULTIPLYER_HEIGHT)
				window_position = (WIDTH-window_size[0]-5*OBJECT_MULTIPLYER_WIDTH, 75*OBJECT_MULTIPLYER_HEIGHT)
				self.upgrading_window_on = True
				flag = False
				for obj in self.additional_objects:
					if obj.name == 'upgrade_window' or obj.name == 'upgrade_tower_button' or obj.name == 'upgrade_shooters_button' or obj.name == 'upgrade_shooters_text' or obj.name == 'upgrade_shooters_text_2' or obj.name == 'settings_window':
						flag = True
					if obj.name == 'upgrade_shooters_text':
						obj.image = self.info_font.render(f'{self.town_shooters[0].upgrade_cost} - {self.town_shooters[0].level + 1}', False, (240, 236, 55))
					if obj.name == 'upgrade_castle_text':
						obj.image = self.info_font.render(f'{int(self.castle.upgrade_cost)} - {self.castle.level + 1}', False, (240, 236, 55))


				if not flag:
					self.additional_objects.append(objects.Window('upgrade_window', images.get_gray_window(window_size), window_position))
					self.additional_objects.append(objects.UpgradeShooterButton((window_position[0]+15*OBJECT_MULTIPLYER_WIDTH, window_position[1]+25*OBJECT_MULTIPLYER_HEIGHT)))
					self.additional_objects.append(objects.Text('upgrade_shooters_text', self.info_font.render(f'{self.town_shooters[0].upgrade_cost} - {self.town_shooters[0].level + 1}', False, (240, 236, 55)), (window_position[0]+18*OBJECT_MULTIPLYER_WIDTH, window_position[1]+25*OBJECT_MULTIPLYER_HEIGHT)))
					self.additional_objects.append(objects.Text('upgrade_shooters_text_2', self.info_font_small.render('Upgrade town shooters', False, (255, 255, 255)), (window_position[0]+15*OBJECT_MULTIPLYER_WIDTH, window_position[1]+8*OBJECT_MULTIPLYER_HEIGHT)))
					
					self.additional_objects.append(objects.UpgradeCastleButton((window_position[0]+15*OBJECT_MULTIPLYER_WIDTH, window_position[1]+UPGRADE_SHOOTER_BUTTON_SIZE[1]*4)))
					self.additional_objects.append(objects.Text('upgrade_castle_text', self.info_font.render(f'{self.castle.upgrade_cost} - {self.castle.level + 1}', False, (240, 236, 55)), (window_position[0]+18*OBJECT_MULTIPLYER_WIDTH, window_position[1]+UPGRADE_SHOOTER_BUTTON_SIZE[1]*4)))
					self.additional_objects.append(objects.Text('upgrade_castle_text_2', self.info_font_small.render('Upgrade Castle', False, (255, 255, 255)), (window_position[0]+15*OBJECT_MULTIPLYER_WIDTH, window_position[1]+(UPGRADE_SHOOTER_BUTTON_SIZE[1]+8)*2 + 20*OBJECT_MULTIPLYER_HEIGHT)))
			if self.in_battle and self.upgrading_window_on:
				remove_list = []
				for obj in self.additional_objects:
					if obj.name == 'upgrade_window' or obj.name == 'upgrade_tower_button' or obj.name == 'upgrade_shooters_button' or obj.name == 'upgrade_shooters_text' or obj.name == 'upgrade_shooters_text_2' or obj.name == 'upgrade_castle_button' or obj.name == 'upgrade_castle_text' or obj.name == 'upgrade_castle_text_2':
						remove_list.append(obj)
				for obj in remove_list:
					self.additional_objects.remove(obj)
				self.upgrading_window_on = False

	async def update_skills_button(self):
		if self.prev_additional_objects == []:
			if not self.in_battle and not self.skills_button_on:
				self.skills_button_on = True

				window_size = (70*OBJECT_MULTIPLYER_WIDTH, 150*OBJECT_MULTIPLYER_HEIGHT)
				button_position = (WIDTH-window_size[0]-100*OBJECT_MULTIPLYER_WIDTH-SKILLS_BUTTON_SIZE[0], 125*OBJECT_MULTIPLYER_HEIGHT)

				self.additional_objects.append(objects.Button('skills_button', images.get_skills_button(), button_position))
			elif self.in_battle:
				self.skills_button_on = False
				for i in self.additional_objects:
					if i.name == 'skills_button':
						self.additional_objects.remove(i)
						break

	async def open_skills_window(self):
		if self.prev_additional_objects == []:
			self.prev_additional_objects = list(self.additional_objects)
			self.additional_objects = []
			self.skills_window_on = True

			window_size = (300*OBJECT_MULTIPLYER_WIDTH, 280*OBJECT_MULTIPLYER_HEIGHT)
			window_position = (WIDTH - 5 - window_size[0], HEIGHT - 5 - window_size[1])
			bonus_gold_skill_button_pos = (window_position[0] + 15*OBJECT_MULTIPLYER_WIDTH, window_position[1]+15*OBJECT_MULTIPLYER_HEIGHT)
			critical_shot_skill_button_pos = (bonus_gold_skill_button_pos[0] + BONUS_GOLD_SKILL_BUTTON_SIZE[0] + 15*OBJECT_MULTIPLYER_WIDTH, bonus_gold_skill_button_pos[1])

			self.additional_objects.append(objects.Image(images.get_gray_window(), window_position, name='skills_window'))
			self.additional_objects.append(objects.Button('bonus_gold_skill_button', images.get_bonus_gold_skill_button(), bonus_gold_skill_button_pos))
			self.additional_objects.append(objects.Button('critical_shot_skill_button', images.get_critical_shot_skill_button(), critical_shot_skill_button_pos))
			self.additional_objects.append(objects.Button('close_button', images.get_close_button(), (window_position[0]+window_size[0]-80*OBJECT_MULTIPLYER_WIDTH, window_position[1])))

	def close_skills_window(self):
		self.additional_objects = list(self.prev_additional_objects)
		self.prev_additional_objects = []
		self.skills_window_on = False

	async def upgrade_skill(self, skill):
		names = [skl.name for skl in self.skills]
		self.upgrading_skill_flag = True

		self.additional_objects = []

		if skill.name in names:
			self.upgrading_skill = self.skills[names.index(skill.name)]
		else:
			self.upgrading_skill = skill

		win_size = (250*OBJECT_MULTIPLYER_WIDTH, 260*OBJECT_MULTIPLYER_HEIGHT)
		win_pos = (WIDTH-win_size[0], 50*OBJECT_MULTIPLYER_HEIGHT)
		self.additional_objects.append(objects.Window('changing_unit_window', images.get_gray_window(win_size), win_pos))
		self.additional_objects.append(objects.Image(pygame.transform.scale(self.upgrading_skill.image, (50*OBJECT_MULTIPLYER_WIDTH, 50*OBJECT_MULTIPLYER_HEIGHT)), (win_pos[0]+15*OBJECT_MULTIPLYER_WIDTH, win_pos[1]+15*OBJECT_MULTIPLYER_HEIGHT), name=f'upgrading_skill {self.upgrading_skill.name}'))
		self.additional_objects.append(objects.Button('close_button', images.get_close_button(), (win_pos[0]-CLOSE_BUTTON_SIZE[0], win_pos[1]-CLOSE_BUTTON_SIZE[1])))

		last_iter = None
		for i in range(len(self.upgrading_skill.description.split('\n'))):
			self.additional_objects.append(objects.Text('upgrading_skill_descripton', self.info_font.render(self.upgrading_skill.description.split('\n')[i], False, (255, 255, 255)), (win_pos[0]+100*OBJECT_MULTIPLYER_WIDTH, win_pos[1]+15*OBJECT_MULTIPLYER_HEIGHT + 15*OBJECT_MULTIPLYER_HEIGHT*i)))
			last_iter = i

		self.additional_objects.append(objects.Text('level', self.info_font_big.render(f'level: {self.upgrading_skill.level}', False, (255, 10, 30)), (win_pos[0] + 85*OBJECT_MULTIPLYER_WIDTH, win_pos[1] + 25*OBJECT_MULTIPLYER_HEIGHT + 15*OBJECT_MULTIPLYER_HEIGHT*last_iter)))

		upgrade_button_pos = (win_pos[0] + 20*OBJECT_MULTIPLYER_WIDTH, win_pos[1]+win_size[1] - 15*OBJECT_MULTIPLYER_HEIGHT - EQUIP_BUTTON_SIZE[1])

		self.additional_objects.append(objects.Button('Upgrade_skill', images.get_text_background((EQUIP_BUTTON_SIZE[0] + 80*OBJECT_MULTIPLYER_WIDTH, EQUIP_BUTTON_SIZE[1])), upgrade_button_pos))
		self.additional_objects.append(objects.Text('Upgrade_skill_text', self.info_font.render(f'{self.upgrading_skill.upgrade_gold_cost} gold and {self.upgrading_skill.upgrade_crystals_cost} crystals - {self.upgrading_skill.level + 1} lvl', False, GOLD_COLOUR), upgrade_button_pos))




	def change_unit(self, unit):
		if self.changing_unit_verb == False:
			self.changing_unit_verb = True
			self.changing_unit_noun = unit

			self.prev_additional_objects = self.additional_objects
			self.additional_objects = []

			self.changing_heroes_list = [[self.total_heroes[i], i] for i in range(len(self.total_heroes)) if self.total_heroes[i].__class__.__name__ != 'Nothing']
			self.changing_scroll_position = 0
			self.current_changing_heroes_list = self.changing_heroes_list[self.changing_scroll_position:5+self.changing_scroll_position:]

			#self.additional_objects.append(objects.Window('changing_unit_window', images.get_gray_window((170*OBJECT_MULTIPLYER_WIDTH, 260*OBJECT_MULTIPLYER_HEIGHT)), (WIDTH-60*OBJECT_MULTIPLYER_WIDTH, HEIGHT-50*OBJECT_MULTIPLYER_HEIGHT)))

			self.update_changing_unit()
		elif self.changing_unit_verb == True:
			self.stop_changing_unit()

	def update_changing_unit(self):
		self.current_changing_heroes_list = self.changing_heroes_list[self.changing_scroll_position:5+self.changing_scroll_position:]
		self.additional_objects = [objects.Window('changing_unit_window', images.get_gray_window((170*OBJECT_MULTIPLYER_WIDTH, 260*OBJECT_MULTIPLYER_HEIGHT)), (WIDTH-170*OBJECT_MULTIPLYER_WIDTH, 50*OBJECT_MULTIPLYER_HEIGHT))]

		iteration = 0
		for obj in self.current_changing_heroes_list:
			win_pos = (self.additional_objects[0].rect.x+5*OBJECT_MULTIPLYER_WIDTH, self.additional_objects[0].rect.y+10*OBJECT_MULTIPLYER_HEIGHT+(35*iteration)*OBJECT_MULTIPLYER_HEIGHT)
			transformation = ()
			self.additional_objects.append(objects.Window(f'changing_element_{iteration}_background', images.get_text_background((150*OBJECT_MULTIPLYER_WIDTH, 35*OBJECT_MULTIPLYER_HEIGHT)), win_pos))
			if obj[0].__class__.__name__ == 'Maradauer':
				transformation = (22*OBJECT_MULTIPLYER_WIDTH, 30*OBJECT_MULTIPLYER_HEIGHT)
			else:
				transformation = (30*OBJECT_MULTIPLYER_WIDTH, 30*OBJECT_MULTIPLYER_HEIGHT)
			self.additional_objects.append(objects.Window(f'changing_hero {obj[1]}', pygame.transform.scale(obj[0].image, transformation), (win_pos[0]+2*OBJECT_MULTIPLYER_WIDTH, win_pos[1]+2*OBJECT_MULTIPLYER_HEIGHT)))
			self.additional_objects.append(objects.Text(f'changing_hero_text {obj[1]}', self.info_font.render(str(f'{obj[0].name}'), False, (255, 255, 255)), (win_pos[0]+7*OBJECT_MULTIPLYER_WIDTH+transformation[0], win_pos[1]+2*OBJECT_MULTIPLYER_HEIGHT)))
			iteration += 1

	def stop_changing_unit(self):
		self.changing_unit_verb = False
		#self.changing_unit_noun = None

		self.additional_objects = list(self.prev_additional_objects)
		self.prev_additional_objects = []

	def upgrade_hero(self, hero_index):
		self.stop_changing_unit()
		self.prev_additional_objects = list(self.additional_objects)
		self.additional_objects = []
		self.upgrading_hero_obj = self.total_heroes[hero_index]

		self.upgrading_hero = True

		upgrade_hero_window_size = (400*OBJECT_MULTIPLYER_WIDTH, 280*OBJECT_MULTIPLYER_HEIGHT)
		upgrade_hero_window_pos = (WIDTH // 2 - upgrade_hero_window_size[0], HEIGHT//2 - upgrade_hero_window_size[1])

		self.additional_objects.append(objects.Window('upgrade_hero_window', images.get_gray_window(upgrade_hero_window_size), upgrade_hero_window_pos))
		self.additional_objects.append(objects.Window('upgrade_hero_image', self.upgrading_hero_obj.image, (upgrade_hero_window_pos[0]+5*OBJECT_MULTIPLYER_WIDTH, upgrade_hero_window_pos[1]+8*OBJECT_MULTIPLYER_HEIGHT)))

		#print(self.additional_objects)

	def update_bonus_gold(self):
		self.bonus_gold = 0
		for skill in self.skills:
			if skill.name == 'BonusGold':
				self.bonus_gold += skill.bonus_percent
				break

	async def update_upgrading_hero(self):
		self.additional_objects = []

		upgrade_hero_window_size = (400*OBJECT_MULTIPLYER_WIDTH, 280*OBJECT_MULTIPLYER_HEIGHT)
		upgrade_hero_window_pos = (WIDTH // 2 - upgrade_hero_window_size[0]//2, HEIGHT//2 - upgrade_hero_window_size[1]//2)
		upgrade_hero_image_pos = (upgrade_hero_window_pos[0]+5*OBJECT_MULTIPLYER_WIDTH, upgrade_hero_window_pos[1]+8*OBJECT_MULTIPLYER_HEIGHT)
		upgrade_hero_image_size = (self.upgrading_hero_obj.size[0]*2, self.upgrading_hero_obj.size[1]*2)
		name_hero_text_pos = (upgrade_hero_image_pos[0]+upgrade_hero_image_size[0]+5*OBJECT_MULTIPLYER_WIDTH, upgrade_hero_image_pos[1]+5*OBJECT_MULTIPLYER_HEIGHT)
		#upgrade_hero_window_pos = (0, 0)

		self.additional_objects.append(objects.Window('upgrade_hero_window', images.get_gray_window(upgrade_hero_window_size), upgrade_hero_window_pos))
		self.additional_objects.append(objects.Window('upgrade_hero_image', pygame.transform.scale(self.upgrading_hero_obj.image, upgrade_hero_image_size), upgrade_hero_image_pos))
		self.additional_objects.append(objects.Button('close_button', images.get_close_button(), (upgrade_hero_window_pos[0]+upgrade_hero_window_size[0], upgrade_hero_window_pos[1])))
		self.additional_objects[-1].rect.center = (self.additional_objects[-1].rect.x, self.additional_objects[-1].rect.y)

		if self.changing_unit_noun == self.upgrading_hero_obj:
			self.additional_objects.append(objects.Button('take_off', images.get_take_off_button(), (upgrade_hero_window_pos[0]+TAKE_OFF_BUTTON_SIZE[0]//4, upgrade_hero_window_pos[1]+upgrade_hero_window_size[1]-TAKE_OFF_BUTTON_SIZE[1] - 5*OBJECT_MULTIPLYER_HEIGHT)))
		else:
			self.additional_objects.append(objects.Button('equip', images.get_equip_button(), (upgrade_hero_window_pos[0]+TAKE_OFF_BUTTON_SIZE[0]//4, upgrade_hero_window_pos[1]+upgrade_hero_window_size[1]-TAKE_OFF_BUTTON_SIZE[1] - 5*OBJECT_MULTIPLYER_HEIGHT)))

		self.additional_objects.append(objects.Text('Name_of_hero', self.info_font_big.render(self.upgrading_hero_obj.name, False, (255, 255, 255)), name_hero_text_pos))

		self.additional_objects.append(objects.Text('Description:', self.info_font.render('Description:', False, (255, 255, 255)), (name_hero_text_pos[0], name_hero_text_pos[1]+50*AVERAGE_MULTIPLYER)))
		if self.upgrading_hero_obj.name == 'Maradauer':
			self.show_maradauer_discription(upgrade_hero_window_size, upgrade_hero_window_pos, upgrade_hero_image_pos, upgrade_hero_image_size, name_hero_text_pos)
		elif self.upgrading_hero_obj.name == 'StimManager':
			self.show_stim_manager_discription(upgrade_hero_window_size, upgrade_hero_window_pos, upgrade_hero_image_pos, upgrade_hero_image_size, name_hero_text_pos)
		elif self.upgrading_hero_obj.name == 'UnitHealer':
			self.show_unit_healer_discription(upgrade_hero_window_size, upgrade_hero_window_pos, upgrade_hero_image_pos, upgrade_hero_image_size, name_hero_text_pos)
		elif self.upgrading_hero_obj.name == 'RocketMan':
			self.show_rocket_man_discription(upgrade_hero_window_size, upgrade_hero_window_pos, upgrade_hero_image_pos, upgrade_hero_image_size, name_hero_text_pos)

		upgrade_hero_button_pos = (upgrade_hero_window_pos[0]+upgrade_hero_window_size[0]-EQUIP_BUTTON_SIZE[0]-10*OBJECT_MULTIPLYER_WIDTH, upgrade_hero_window_pos[1]-EQUIP_BUTTON_SIZE[1]-5*OBJECT_MULTIPLYER_HEIGHT+upgrade_hero_window_size[1])

		self.additional_objects.append(objects.Button('Upgrade_hero', images.get_text_background(EQUIP_BUTTON_SIZE), upgrade_hero_button_pos))
		self.additional_objects.append(objects.Text('Upgrade_cost', self.info_font_big.render(f'{self.upgrading_hero_obj.upgrade_cost} - {self.upgrading_hero_obj.level + 1}', False, GOLD_COLOUR), upgrade_hero_button_pos))

	async def close_everything(self):
		if self.prev_additional_objects != []:
			if self.upgrading_hero:
				self.stop_upgrading_hero()
			elif self.trading:
				self.stop_trading()
			elif self.skills_window_on:
				self.close_skills_window()
			else: self.additional_objects = []
			#self.additional_objects = list(self.prev_additional_objects)
			#self.prev_additional_objects = []
		else: pass

	def show_maradauer_discription(self, upgrade_hero_window_size, upgrade_hero_window_pos, upgrade_hero_image_pos, upgrade_hero_image_size, name_hero_text_pos):
		self.additional_objects.append(objects.Text('Create group of 6 range', self.info_font.render('Create group of 6 range', False, (255, 255, 255)), (name_hero_text_pos[0], name_hero_text_pos[1]+65*AVERAGE_MULTIPLYER)))
		self.additional_objects.append(objects.Text('attack units for limited time', self.info_font.render('attack units for limited time', False, (255, 255, 255)), (name_hero_text_pos[0], name_hero_text_pos[1]+80*AVERAGE_MULTIPLYER)))
		self.additional_objects.append(objects.Text('Damage', self.info_font_big.render(str(self.upgrading_hero_obj.damage), False, (255, 15, 15)), (upgrade_hero_image_pos[0]+20*AVERAGE_MULTIPLYER, upgrade_hero_image_pos[1]+upgrade_hero_image_size[1]+40*AVERAGE_MULTIPLYER)))

	def show_stim_manager_discription(self, upgrade_hero_window_size, upgrade_hero_window_pos, upgrade_hero_image_pos, upgrade_hero_image_size, name_hero_text_pos):
		self.additional_objects.append(objects.Text('Boost attack speed of town shooters', self.info_font.render('Boost attack speed of town shooters', False, (255, 255, 255)), (name_hero_text_pos[0], name_hero_text_pos[1]+65*AVERAGE_MULTIPLYER)))
		self.additional_objects.append(objects.Text('on 60%, for limited time', self.info_font.render('on 60%, for limited time', False, (255, 255, 255)), (name_hero_text_pos[0], name_hero_text_pos[1]+80*AVERAGE_MULTIPLYER)))
		self.additional_objects.append(objects.Text('Ability_duration', self.info_font_big.render('Ability duration - '+str(self.upgrading_hero_obj.stimpack_speed/FPS)+' sec', False, (150, 150, 255)), (upgrade_hero_image_pos[0]+20*AVERAGE_MULTIPLYER, upgrade_hero_image_pos[1]+upgrade_hero_image_size[1]+40*AVERAGE_MULTIPLYER)))

	def show_unit_healer_discription(self, upgrade_hero_window_size, upgrade_hero_window_pos, upgrade_hero_image_pos, upgrade_hero_image_size, name_hero_text_pos):
		self.additional_objects.append(objects.Text('Heal all allies units', self.info_font.render('Heal all allies units', False, (255, 255, 255)), (name_hero_text_pos[0], name_hero_text_pos[1]+65*AVERAGE_MULTIPLYER)))
		self.additional_objects.append(objects.Text('Healing', self.info_font_big.render('Healing - '+str(self.upgrading_hero_obj.heal)+' hp', False, (150, 150, 255)), (upgrade_hero_image_pos[0]+20*AVERAGE_MULTIPLYER, upgrade_hero_image_pos[1]+upgrade_hero_image_size[1]+40*AVERAGE_MULTIPLYER)))

	def show_rocket_man_discription(self, upgrade_hero_window_size, upgrade_hero_window_pos, upgrade_hero_image_pos, upgrade_hero_image_size, name_hero_text_pos):
		self.additional_objects.append(objects.Text('Makes five rocket shoots', self.info_font.render('Makes five rocket shoots', False, (255, 255, 255)), (name_hero_text_pos[0], name_hero_text_pos[1]+65*AVERAGE_MULTIPLYER)))
		self.additional_objects.append(objects.Text('Damage', self.info_font_big.render(str(self.upgrading_hero_obj.damage), False, (255, 15, 15)), (upgrade_hero_image_pos[0]+20*AVERAGE_MULTIPLYER, upgrade_hero_image_pos[1]+upgrade_hero_image_size[1]+40*AVERAGE_MULTIPLYER)))

	def stop_upgrading_hero(self):
		self.upgrading_hero = False
		self.upgrading_hero_obj = None
		self.additional_objects = list(self.prev_additional_objects)
		self.prev_additional_objects = []

	def upgrade_hero_action(self):
		if self.gold - self.upgrading_hero_obj.upgrade_cost >= 0:
			self.gold -= self.upgrading_hero_obj.upgrade_cost
			self.upgrading_hero_obj.new_level()
			self.total_heroes[self.total_heroes.index(self.upgrading_hero_obj)] = self.upgrading_hero_obj
			try:
				self.heroes[self.heroes.index(self.upgrading_hero_obj)] = self.upgrading_hero_obj
			except Exception as e: print(e)
		else: print('not enought gold')

	def update_targetting(self):
		self.additional_objects = []
		self.additional_objects.append(objects.Image(images.get_close_button(), (pygame.mouse.get_pos()[0], self.castle.rect.y+self.castle.size[1]-20*OBJECT_MULTIPLYER_HEIGHT)))
		if self.hero_target_position != ():
			self.targetting_hero.attack(self)
			self.additional_objects = list(self.targetting_prev_additional_objects)
			self.hero_target_position = ()
			self.targetting = False

	def start_targetting(self):
		self.targetting_prev_additional_objects = list(self.additional_objects)
		self.targetting = True

	async def goto_town(self):
		if self.global_location != 'Town':
			self.prev_additional_objects = list(self.additional_objects)
			self.additional_objects = []
			self.global_location = 'Town'

			await self.init_town()

	async def goto_castle(self):
		if self.global_location != "Castle":
			self.additional_objects = list(self.prev_additional_objects)
			self.prev_additional_objects = []
			self.global_location = 'Castle'

	async def init_town(self):
		self.ground_objects = [GroundObjects.Market(3)]

	def start_trading(self):
		self.trading = True
		self.trade_opened = False
		self.special_buttons_avalible = False

	def stop_trading(self):
		self.additional_objects = []
		self.trading = False
		self.special_buttons_avalible = True

	async def update_trading(self):
		window_size = (400*OBJECT_MULTIPLYER_WIDTH, 200*OBJECT_MULTIPLYER_HEIGHT)
		window_position = (WIDTH//2 - window_size[0]//2, HEIGHT//2 - window_size[1]//2)
		if not self.trade_opened:
			self.additional_objects = []

			self.additional_objects.append(objects.Window('trading_window', images.get_gray_window(window_size), window_position))
			self.additional_objects.append(objects.Button('close_button', images.get_close_button(), (window_position[0]+window_size[0], window_position[1])))
			self.additional_objects.append(objects.Image(images.get_crystal((50*AVERAGE_MULTIPLYER, 50*AVERAGE_MULTIPLYER)), (window_position[0]+10*OBJECT_MULTIPLYER_WIDTH, window_position[1]+10*OBJECT_MULTIPLYER_HEIGHT)))
			self.additional_objects.append(objects.Button('buy_crystal', images.get_buy_button(), (window_position[0]+30*OBJECT_MULTIPLYER_WIDTH, window_position[1]+window_size[1]-BUY_BUTTON_SIZE[1]-5*OBJECT_MULTIPLYER_HEIGHT)))
			self.additional_objects.append(objects.Button('sell_crystal', images.get_sell_button(), (window_position[0]+window_size[0]-30*OBJECT_MULTIPLYER_WIDTH-SELL_BUTTON_SIZE[0], window_position[1]+window_size[1]-SELL_BUTTON_SIZE[1]-5*OBJECT_MULTIPLYER_HEIGHT)))
			self.additional_objects.append(self.on_stats_traiding_obj)
			self.additional_objects.append(objects.Text('cost_of_crystal', self.info_font_big.render(str(self.cost_of_crystal), False, GOLD_COLOUR), (window_position[0]+(50+50)*OBJECT_MULTIPLYER_WIDTH, window_position[1]+20*OBJECT_MULTIPLYER_HEIGHT)))
			self.trade_opened = True
		self.additional_objects[-1] = objects.Text('cost_of_crystal', self.info_font_big.render(str(self.cost_of_crystal), False, GOLD_COLOUR), (window_position[0]+(50+50)*OBJECT_MULTIPLYER_WIDTH, window_position[1]+20*OBJECT_MULTIPLYER_HEIGHT))
		self.additional_objects[-2] = self.on_stats_traiding_obj

	async def update_cost_of_crystal(self):
		local_cost = 0

		ch = random.randint(1, 3)
		if ch == 2 or ch == 3 or ch == 4:
			if self.cost_of_crystal - self.cost_of_crystal//3 > 0:
				local_cost -= random.randint(0, self.cost_of_crystal-random.randrange(0, (self.cost_of_crystal//2+1)))
			else: local_cost = 10
		else:
			if self.cost_of_crystal//3+1 >= 0 and self.cost_of_crystal > 0:
				local_cost += random.randint(0, self.cost_of_crystal+random.randrange(0, self.cost_of_crystal//3+1))
			else: local_cost = 10

		ch_2 = random.randint(1, 3)
		if ch_2 == 1:
			local_cost += self.cost_of_crystal // 2 + 50
		#elif ch == 2:
		#	self.cost_of_crystal -= self.cost_of_crystal // 4 + 50

		if self.cost_of_crystal + local_cost <= 0:
			local_cost = 10

		window_size = (400*OBJECT_MULTIPLYER_WIDTH, 200*OBJECT_MULTIPLYER_HEIGHT)
		window_position = (WIDTH//2 - window_size[0]//2, HEIGHT//2 - window_size[1]//2)
		if local_cost == 0:
			self.on_stats_traiding_obj = objects.Image(images.get_trading_minus(), (window_position[0]+90*OBJECT_MULTIPLYER_WIDTH, window_position[1]+70*OBJECT_MULTIPLYER_HEIGHT))
		elif local_cost < 0:
			self.on_stats_traiding_obj = objects.Image(images.get_trading_fall(), (window_position[0]+90*OBJECT_MULTIPLYER_WIDTH, window_position[1]+70*OBJECT_MULTIPLYER_HEIGHT))
		elif local_cost > 0:
			self.on_stats_traiding_obj = objects.Image(images.get_trading_raise(), (window_position[0]+90*OBJECT_MULTIPLYER_WIDTH, window_position[1]+70*OBJECT_MULTIPLYER_HEIGHT))
		self.cost_of_crystal += local_cost

	def sell_crystal(self):
		if self.crystal > 0:
			self.crystal -= 1
			self.gold += self.cost_of_crystal
			self.cost_of_crystal -= math.ceil(self.cost_of_crystal * 0.03)
		else: print('not enought crystals')

	def buy_crystal(self):
		if self.gold - self.cost_of_crystal >= 0:
			self.gold -= self.cost_of_crystal
			self.crystal += 1
			self.cost_of_crystal += math.ceil(self.cost_of_crystal * 0.01)
		else: print('not enought gold')