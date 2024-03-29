from datetime import datetime
print('GrowWord - made by Wokzy and Arter')
print('Version - 0.03.0')
print('Loading...')
load_time = datetime.now()
import pygame, sys, random, images, scripts.castle, scripts.GameFunctions, asyncio, scripts.Town_shooters
from constants import *
from scripts import objects, heroes


pygame.init()
pygame.font.init()

class GrowWord:
	def __init__(self, gf):
		self.screen = pygame.display.set_mode(WINDOW_RESOLUTION)#, vsync=1)
		pygame.display.set_caption('GrowWord')

		self.road_image = images.get_road()
		self.road_rect = self.road_image.get_rect()

		self.init_hitpoints()
		self.init_mana()
		if gf.town_shooters == []:
			self.init_townshooters()

		self.info_font = pygame.font.SysFont('Comic Sans MS', INFO_FONT_SIZE)

		self.clock = pygame.time.Clock()
		self.iteration = 0 # 60 Iterations - 1 second

	async def main(self, gf):
		self.road_rect.center = (WIDTH // 2, HEIGHT - ROAD_SIZE[1]//2)
		self.hpbar_rect = self.hpbar_place
		self.manabar_rect = self.manabar_place

		gf.init_objects()

		while True:
			self.screen.fill((230, 236, 242))

			await self.update_event()

			if not gf.targetting:
				await self.update(gf)

			self.mana_text = self.info_font.render('Mana: {}'.format(str(gf.castle.mana)), False, (0, 0, 0))
			self.hp_text = self.info_font.render('HP: {}'.format(str(gf.castle.hp)), False, (0, 0, 0))

			await self.blit_objects()

			self.clock.tick(FPS) #pygame.time.delay(8)
			self.iteration += 1
			pygame.display.update()
			pygame.event.pump()



	async def update(self, gf):
		# Updating HP

		self.hpbar_size = await gf.castle.update_hpbar_size(self.hpbar_size)
		self.hpbar_image = pygame.transform.scale(images.HPBAR_IMAGE, self.hpbar_size)
		self.hpbar_rect = self.hpbar_image.get_rect()
		self.hpbar_rect = self.hpbar_place

		# Updating Mana

		self.manabar_size = await gf.castle.update_manabar_size(self.manabar_size)
		self.manabar_image = pygame.transform.scale(images.MANABAR_IMAGE, self.manabar_size)
		self.manabar_rect = self.manabar_image.get_rect()
		self.manabar_rect = self.manabar_place


		gf.castle.mana_add_iterations += 1
		gf.castle.mana_add_iterations_slide += 1
		if gf.castle.mana + gf.castle.total_mana // 125 <= gf.castle.total_mana and gf.castle.mana_add_iterations >= MANA_ADD_TIMER:
			if gf.castle.mana_add_iterations_slide>= MANA_ADD_TIMER / (gf.castle.total_mana // 125):
				gf.castle.mana += 1
				self.mana_add_iterations_slide = 0
			gf.castle.mana_add_iterations = 0
		elif gf.castle.mana + gf.castle.total_mana // 125 > gf.castle.total_mana:
			gf.castle.mana = gf.castle.total_mana
		'''
		if gf.castle.hp + 1 <= gf.castle.total_hp:
			gf.castle.hp += 1
		else:
			gf.castle.hp = gf.castle.total_hp
		'''
		
		if not gf.in_battle:
			gf.castle.hp = gf.castle.total_hp
			gf.castle.mana = gf.castle.total_mana
			for i in gf.town_shooters:
				i.image = i.stay_image

		if gf.in_battle:
			self.update_townshooters(gf)
			self.update_allies_units(gf)
			if gf.boss != None:
				gf.boss.update(gf)
		elif not gf.in_battle:
			if gf.town_shooters[0].on_stimpack:
				for town_shooter in gf.town_shooters:
					town_shooter.stop_stimpack()

		self.update_heroes()

		await self.update_textes()
		if self.iteration%(FPS*5) == 0:
			await gf.update_cost_of_crystal()
		await self.update_special_buttons()


		if self.iteration%(FPS*60) == 0:
			await gf.save_state()

		if self.iteration == 3628800:
			self.iteration = 0
			gf.gold = int(gf.gold)

	async def blit_objects(self):
		self.screen.blit(self.road_image, self.road_rect)

		if gf.global_location == 'Castle':
			self.screen.blit(gf.castle.castle_image, gf.castle.castle_rect)
			if gf.special_buttons_avalible:
				self.screen.blit(gf.special_buttons['goto_town'].image, gf.special_buttons['goto_town'].rect)

			await self.blit_hitpoints()
			await self.blit_mana()
			await self.blit_townshooters()
			await self.blit_heroes()

			if gf.in_battle:
				if not gf.targetting:
					await gf.update_battle()
				await self.blit_enemyes()
				await self.blit_allies_heroes()
		else:
			for obj in gf.ground_objects:
				self.screen.blit(obj.image, obj.rect)
			if gf.special_buttons_avalible:
				self.screen.blit(gf.special_buttons['goto_castle'].image, gf.special_buttons['goto_castle'].rect)

		await gf.find_blitting_object()

		for obj in gf.additional_objects:
			self.screen.blit(obj.image, obj.rect)
			if obj.__class__.__name__ == 'TextInput':
				self.screen.blit(obj.text.image, obj.text.rect)
			#if obj.__class__.__name__ == 'Text':
			#	self.screen.blit(obj.image, obj.rect)

		for obj in gf.info_objects:
			self.screen.blit(obj.image, obj.rect)

		if gf.in_battle:
			for obj in gf.battle_objects:
				self.screen.blit(obj.image, obj.rect)
			self.screen.blit(gf.wave_bar_background.image, gf.wave_bar_background.rect)
			self.screen.blit(gf.wave_bar.image, gf.wave_bar.rect)
			self.screen.blit(gf.wave_text.image, gf.wave_text.rect)
			if gf.boss != None:
				self.screen.blit(gf.boss.image, gf.boss.rect)
			#print(gf.wave_bar)

	def update_heroes(self):
		for hero in gf.heroes:
			hero.update(gf)
			if hero.__class__.__name__ != 'Nothing':
				if not gf.in_battle:
					hero.cooldown_iteration = hero.cooldown

	def init_hitpoints(self):
		self.hpbar_image = images.get_hp_bar()
		self.hpbar_rect = self.hpbar_image.get_rect()
		self.hpbar_size = DEFAULT_HPBAR_SIZE
		self.hpbar_place = (WIDTH - self.hpbar_size[0]*2, 2*OBJECT_MULTIPLYER_HEIGHT)

		self.hpbar_background_image = images.get_hp_bar_background()
		self.hpbar_background_rect = self.hpbar_place

	def init_mana(self):
		self.manabar_image = images.get_mana_bar()
		self.manabar_rect = self.manabar_image.get_rect()
		self.manabar_size = DEFAULT_MANABAR_SIZE
		self.manabar_place = (WIDTH - self.manabar_size[0], 2*OBJECT_MULTIPLYER_HEIGHT)

		self.manabar_background_image = images.get_mana_bar_background()
		self.manabar_background_rect = self.manabar_place

	def init_townshooters(self):
		if gf.town_shooters == []:
			for i in range(4):
				for g in range(5):
					gf.town_shooters.append(scripts.Town_shooters.TownShooter(1, images.get_town_shooter(), g, i))

	def update_townshooters(self, gf):
		for shooter in gf.town_shooters:
			action = shooter.update(gf.battle_heroes, gf)
			if action == 'attack':
				dmg = shooter.damage
				for i in gf.skills:
					if i.name == 'CriticalShot':
						if random.randint(0, 100) <= i.chance:
							#print(f'CRIT! - {dmg} dmg ', end='')
							dmg *= 2.25
							#print(f'- {dmg}')
						break
				if not shooter.target_is_boss:
					gf.battle_heroes[gf.battle_heroes.index(shooter.target)].attacking_me_shooters += 1
					gf.battle_heroes[gf.battle_heroes.index(shooter.target)].hp -= int(dmg)
				else:
					if gf.boss != None:
						gf.boss.hp -= int(dmg * gf.boss.armor_multiplyer)

	def update_allies_units(self, gf):
		rm_units = []

		for unit in gf.allies_units:
			action = unit.update(gf)
			if not unit.alive:
				rm_units.append(unit)
				continue
			if action == 'attack':
				if unit.target == gf.boss:
					if gf.boss != None:
						gf.boss.hp -= int(unit.damage * gf.boss.armor_multiplyer)
				else:
					gf.battle_heroes[gf.battle_heroes.index(unit.target)].hp -= unit.damage

		for unit in rm_units:
			gf.allies_units.remove(unit)

	async def update_textes(self):
		for obj in gf.info_objects:
			if obj.name == 'gold_text':
				#a = []
				#for i in range(len(str(gf.gold+100000))):
				#	if i%3 != 0:
				#		a.append(str(gf.gold+100000)[i])
				#	else: a.append(str(gf.gold+100000)[i]+'.')
				#a[-1] = a[-1][:1:]
				obj.image = self.info_font.render('G '+str(gf.gold), False, (240, 236, 55))
			elif obj.name == 'crystal_text':
				obj.image = self.info_font.render(str(gf.crystal), False, (25, 210 , 25))

	async def update_special_buttons(self):
		if not gf.special_buttons_avalible:
			if not gf.in_battle and gf.prev_additional_objects == [] and gf.global_location == 'Castle':
				gf.special_buttons_avalible = True
		elif gf.special_buttons_avalible:
			if gf.in_battle or gf.prev_additional_objects != [] and gf.global_location == 'Castle':
				gf.special_buttons_avalible = False
			if gf.global_location == 'Town' and gf.additional_objects != []:
				gf.special_buttons_avalible = False

	async def blit_heroes(self):
		for hero in gf.heroes:
			self.screen.blit(hero.image, hero.rect)
			self.screen.blit(hero.cooldown_background_bar_image, hero.cooldown_background_bar_rect)
			self.screen.blit(hero.cooldown_bar_image, hero.cooldown_bar_rect)
			self.screen.blit(images.get_hero_background(), hero.rect)

	async def blit_allies_heroes(self):
		for unit in gf.allies_units:
			self.screen.blit(unit.image, unit.rect)
			try:
				self.screen.blit(unit.hp_bar_background_image, unit.hp_bar_background_rect)
				self.screen.blit(unit.hp_bar_image, unit.hp_bar_rect)
			except: pass

	async def blit_hitpoints(self):
		self.screen.blit(self.hpbar_background_image, self.hpbar_background_rect)
		self.screen.blit(self.hpbar_image, self.hpbar_rect)
		self.screen.blit(self.hp_text, (self.hpbar_place[0]+2*OBJECT_MULTIPLYER_WIDTH, self.hpbar_place[1]))

	async def blit_mana(self):
		self.screen.blit(self.manabar_background_image, self.manabar_background_rect)
		self.screen.blit(self.manabar_image, self.manabar_rect)
		self.screen.blit(self.mana_text, (self.manabar_place[0]+2*OBJECT_MULTIPLYER_WIDTH, self.manabar_place[1]))

	async def blit_enemyes(self):
		for enemy in gf.battle_heroes:
			self.screen.blit(enemy.image, enemy.rect)
			self.screen.blit(enemy.hp_bar_background_image, enemy.hp_bar_background_rect)
			self.screen.blit(enemy.hp_bar_image, enemy.hp_bar_rect)

	async def blit_townshooters(self):
		for shooter in gf.town_shooters:
			self.screen.blit(shooter.image, shooter.rect)
		if gf.town_shooters[0].stimpack_animation:
			for shooter in gf.town_shooters:
				if shooter.stimpack_animation_iterations >= shooter.stimpack_animation_speed:
					shooter.stimpack_animation = False
				else:
					if shooter.on_stimpack:
						self.screen.blit(images.get_stim_on(), (shooter.rect.center[0]-3*OBJECT_MULTIPLYER_WIDTH, shooter.rect.y - STIM_ON_SIZE[1]))
					else:
						self.screen.blit(images.get_stim_off(), (shooter.rect.center[0]-3*OBJECT_MULTIPLYER_WIDTH, shooter.rect.y - STIM_OFF_SIZE[1]))
					shooter.stimpack_animation_iterations += 1

	async def update_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if gf.enter_in_text_input:
					await gf.entering_in_text_input(event)
					continue
				if gf.global_location == 'Castle':
					try:
						if event.key == pygame.K_1:
								gf.heroes[0].action(gf)
						elif event.key == pygame.K_2:
								gf.heroes[1].action(gf)
						elif event.key == pygame.K_3:
								gf.heroes[2].action(gf)
						elif event.key == pygame.K_4:
								gf.heroes[3].action(gf)
						if not gf.in_battle and event.key == pygame.K_SPACE:
							await gf.start_battle()
						elif event.key == pygame.K_t and not gf.in_battle and gf.special_buttons_avalible:
							await gf.goto_town()
					except Exception as e:
						print(e)
				elif gf.global_location == 'Town':
					if event.key == pygame.K_c and not gf.in_battle and gf.special_buttons_avalible:
						await gf.goto_castle()
				#elif event.key == pygame.K_7:
				#	await gf.goto_town()
				#elif event.key == pygame.K_8:
				#	await gf.goto_castle()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mos_pos = pygame.mouse.get_pos()
				if gf.special_buttons_avalible:
					if gf.special_buttons['goto_castle'].rect.collidepoint(mos_pos):
						await gf.special_buttons['goto_castle'].action(gf)
						continue
					elif gf.special_buttons['goto_town'].rect.collidepoint(mos_pos):
						await gf.special_buttons['goto_town'].action(gf)
						continue
				if gf.targetting:
					if not mos_pos[0] < gf.castle.rect.x + gf.castle.size[0]:
						gf.hero_target_position = mos_pos
					continue
				flag = False
				for obj in gf.additional_objects[::-1]:
					#try:
					if obj.__class__.__name__ != 'Text' and obj.rect.collidepoint(mos_pos) and event.button != 4 and event.button != 5:
						await obj.action(gf)
						if obj.__class__.__name__ == 'TextInput':
							gf.text_input_obj = obj
							gf.text_input_index = gf.additional_objects.index(obj)
							gf.enter_in_text_input = True
						flag = True
						break
					#except Exception as e:
					#	print(e)
				if gf.global_location == 'Town':
					for obj in gf.ground_objects:
						if obj.rect.collidepoint(mos_pos):
							await obj.action(gf)
				if gf.enter_in_text_input and not gf.text_input_obj.rect.collidepoint(mos_pos):
					gf.text_input_obj = None
					gf.enter_in_text_input = False
				if not flag:
					if gf.global_location == 'Castle':
						for hero in gf.heroes:
							if hero.rect.collidepoint(mos_pos):
								hero.action(gf)
								break
				if gf.changing_unit_verb:
					if event.button == 4:
						if gf.changing_scroll_position > 0:
							gf.changing_scroll_position -= 1
					elif event.button == 5:
						if gf.changing_scroll_position < len(gf.changing_heroes_list):
							gf.changing_scroll_position += 1
					gf.update_changing_unit()



gf = scripts.GameFunctions.GameFunctions()

async def start():
	print(f'Loaded by {(datetime.now() - load_time).total_seconds()} sec')
	print('GL HF!')
	await GrowWord(gf).main(gf)

asyncio.run(start())