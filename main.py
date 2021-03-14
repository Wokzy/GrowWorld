import pygame, sys, random, images, scripts.castle, scripts.GameFunctions, asyncio, scripts.Town_shooters
from constants import *
from datetime import datetime
from scripts import objects


pygame.init()
pygame.font.init()

class GrowWord:
	def __init__(self, gf):
		self.screen = pygame.display.set_mode(WINDOW_RESOLUTION)

		self.castle = scripts.castle.Castle()

		self.wave = 1

		self.road_image = images.get_road()
		self.road_rect = self.road_image.get_rect()
		self.town_shooters = []

		self.init_hitpoints()
		self.init_mana()
		self.init_townshooters()

		self.info_font = pygame.font.SysFont('Comic Sans MS', INFO_FONT_SIZE)

		self.clock = pygame.time.Clock()

	async def main(self, gf):
		self.castle.castle_rect.x = 100*OBJECT_MULTIPLYER_WIDTH
		self.castle.castle_rect.y = HEIGHT - CASTLE_SIZE[1] - 80 * AVERAGE_MULTIPLYER
		self.road_rect.center = (WIDTH // 2, HEIGHT - ROAD_SIZE[1]//2)
		self.hpbar_rect = self.hpbar_place
		self.manabar_rect = self.manabar_place

		while True:
			self.screen.fill((230, 236, 242))

			await self.update_event()

			await self.update()

			self.mana_text = self.info_font.render('Mana: {}'.format(str(self.castle.mana)), False, (0, 0, 0))
			self.hp_text = self.info_font.render('HP: {}'.format(str(self.castle.hp)), False, (0, 0, 0))

			await self.blit_objects()

			self.clock.tick(FPS) #pygame.time.delay(8)
			pygame.display.update()
			pygame.event.pump()



	async def update(self):
		# Updating HP

		self.hpbar_size = await self.castle.update_hpbar_size(self.hpbar_size)
		self.hpbar_image = pygame.transform.scale(images.HPBAR_IMAGE, self.hpbar_size)
		self.hpbar_rect = self.hpbar_image.get_rect()
		self.hpbar_rect = self.hpbar_place

		# Updating Mana

		self.manabar_size = await self.castle.update_manabar_size(self.manabar_size)
		self.manabar_image = pygame.transform.scale(images.MANABAR_IMAGE, self.manabar_size)
		self.manabar_rect = self.manabar_image.get_rect()
		self.manabar_rect = self.manabar_place

		if self.castle.mana + self.castle.total_mana // 125 <= self.castle.total_mana and (datetime.now() - self.castle.mana_add_timer).total_seconds() >= MANA_ADD_TIMER:
			if (datetime.now() - self.castle.mana_add_timer_slide).total_seconds() >= MANA_ADD_TIMER / (self.castle.total_mana // 125):
				self.castle.mana += 1
				self.mana_add_timer_slide = datetime.now()
			self.castle.mana_add_timer = datetime.now()
		elif self.castle.mana + self.castle.total_mana // 125 > self.castle.total_mana:
			self.castle.mana = self.castle.total_mana
		'''
		if self.castle.hp + 1 <= self.castle.total_hp:
			self.castle.hp += 1
		else:
			self.castle.hp = self.castle.total_hp
		'''
		
		if not gf.in_battle:
			self.castle.hp = self.castle.total_hp
			self.castle.mana = self.castle.total_mana
			for i in self.town_shooters:
				i.image = i.stay_image

		if gf.in_battle:
			await self.update_townshooters()

	async def blit_objects(self):
		self.screen.blit(self.road_image, self.road_rect)
		self.screen.blit(self.castle.castle_image, self.castle.castle_rect)

		await self.blit_hitpoints()
		await self.blit_mana()
		await self.blit_townshooters()

		if gf.in_battle:
			await gf.update_battle(self.castle)
			await self.blit_enemyes()

		await gf.find_blitting_object()

		for obj in gf.additional_objects:
			self.screen.blit(obj.image, obj.rect)
			if obj.__class__.__name__ == 'TextInput':
				self.screen.blit(obj.text.image, obj.text.rect)

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
		for i in range(4):
			for g in range(5):
				self.town_shooters.append(scripts.Town_shooters.TownShooter(1, images.get_town_shooter(), g, i))

	async def update_townshooters(self):
		for shooter in self.town_shooters:
			action = shooter.update(gf.battle_heroes)
			if action == 'attack':
				gf.battle_heroes[gf.battle_heroes.index(shooter.target)].hp -= shooter.damage
				#gf.battle_heroes[gf.battle_heroes.index(shooter.target)].attacking_me_shooters += 1

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
		for shooter in self.town_shooters:
			self.screen.blit(shooter.image, shooter.rect)

	async def update_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if gf.enter_in_text_input:
					await gf.entering_in_text_input(event)
				elif event.key == pygame.K_1 and self.castle.hp - 100 >= 0:
					self.castle.hp -= 100
				elif event.key == pygame.K_2 and self.castle.mana - 100 >= 0:
					self.castle.mana -= 100
				elif event.key == pygame.K_3 and not gf.in_battle:
					await gf.start_battle(self.wave)
				elif event.key == pygame.K_5 and gf.in_battle:
					gf.battle_heroes[random.randint(0, len(gf.battle_heroes)-1)].bite(5)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mos_pos = pygame.mouse.get_pos()
				for obj in gf.additional_objects[::-1]:
					try:
						if obj.rect.collidepoint(mos_pos):
							await obj.action(gf)
							if obj.__class__.__name__ == 'TextInput':
								gf.text_input_obj = obj
								gf.text_input_index = gf.additional_objects.index(obj)
								gf.enter_in_text_input = True
							break
					except Exception as e: print(e)
				if gf.enter_in_text_input and not gf.text_input_obj.rect.collidepoint(mos_pos):
					gf.text_input_obj = None
					gf.enter_in_text_input = False



gf = scripts.GameFunctions.GameFunctions()

async def start():
	await GrowWord(gf).main(gf)

asyncio.run(start())