# This script load and init images of objects and also their skins, animations and etc.
import pygame
from constants import *

def get_castle(skin='black'):
	if skin == 'black':
		img = pygame.image.load('sprites/castles/new_castle.png')
		return pygame.transform.scale(img, CASTLE_SIZE)


def get_road(skin='sand'):
	if skin == 'sand':
		return pygame.transform.scale(pygame.image.load('sprites/roads/road.png'), ROAD_SIZE)

def get_hp_bar():
	global HPBAR_IMAGE

	if HPBAR_IMAGE == None:
		HPBAR_IMAGE = pygame.transform.scale(pygame.image.load('sprites/bars/hp_bar.png'), DEFAULT_HPBAR_SIZE)
	return HPBAR_IMAGE

def get_mana_bar():
	global MANABAR_IMAGE

	if MANABAR_IMAGE == None:
		MANABAR_IMAGE = pygame.transform.scale(pygame.image.load('sprites/bars/mana_bar.png'), DEFAULT_MANABAR_SIZE)
	return MANABAR_IMAGE

def get_hp_bar_background():
	global HPBAR_BACKGROUND_IMAGE

	if HPBAR_BACKGROUND_IMAGE == None:
		HPBAR_BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load('sprites/bars/background_bar.png'), HPBAR_BACKGROUND_SIZE)
	return HPBAR_BACKGROUND_IMAGE

def get_mana_bar_background():
	return pygame.transform.scale(pygame.image.load('sprites/bars/background_bar.png'), MANABAR_BACKGROUND_SIZE)

def get_monster():
	global MONSTER_IMAGE

	if MONSTER_IMAGE == None:
		MONSTER_IMAGE = pygame.transform.scale(pygame.image.load('sprites/enemyes/monster.png'), MONSTER_SIZE)
	return MONSTER_IMAGE

def get_town_shooter():
	global TOWN_SHOOTER_IMAGES

	if TOWN_SHOOTER_IMAGES == None:
		size = (23*OBJECT_MULTIPLYER_WIDTH, 21*OBJECT_MULTIPLYER_HEIGHT)
		shoot_images = [pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_1.png'), size),
						pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_2.png'), size),
						pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_3.png'), size),]
						#pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_4.png'), size),]
		TOWN_SHOOTER_IMAGES = {'stay_image': pygame.transform.scale(pygame.image.load('sprites/marine/marine_stay.png'), TOWN_SHOOTER_SIZE), \
								'shoot_image': shoot_images, 'total_size': size}
	return TOWN_SHOOTER_IMAGES

def get_settings_button():
	global SETTINGS_BUTTON_IMAGE

	if SETTINGS_BUTTON_IMAGE == None:
		SETTINGS_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load('sprites/buttons/gear.png'), SETTINGS_BUTTON_SIZE)
	return SETTINGS_BUTTON_IMAGE

def get_settings_window():
	global SETTINGS_WINDOW_IMAGE

	if SETTINGS_WINDOW_IMAGE == None:
		SETTINGS_WINDOW_IMAGE = pygame.transform.scale(pygame.image.load('sprites/windows/settings_window.png'), SETTINGS_WINDOW_SIZE)
	return SETTINGS_WINDOW_IMAGE

def get_text_input(size):
	global TEXT_INPUT_IMAGE

	if TEXT_INPUT_IMAGE == None:
		TEXT_INPUT_IMAGE = pygame.transform.scale(pygame.image.load('sprites/text_input.png'), size)
	return TEXT_INPUT_IMAGE

def get_apply_settings_button():
	global APPLY_SETTINGS_BUTTON

	if APPLY_SETTINGS_BUTTON == None:
		APPLY_SETTINGS_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/apply.png'), APPLY_SETTIGS_BUTTON_SIZE)
	return APPLY_SETTINGS_BUTTON

def get_fight_button():
	global FIGHT_BUTTON

	if FIGHT_BUTTON == None:
		FIGHT_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/fight.png'), FIGHT_BUTTON_SIZE)
	return FIGHT_BUTTON

def get_stim_on():
	global STIM_ON

	if STIM_ON == None:
		STIM_ON = pygame.transform.scale(pygame.image.load('sprites/flags/stim_on.png'), STIM_ON_SIZE)
	return STIM_ON

def get_stim_off():
	global STIM_OFF

	if STIM_OFF == None:
		STIM_OFF = pygame.transform.scale(pygame.image.load('sprites/flags/stim_off.png'), STIM_OFF_SIZE)
	return STIM_OFF

def get_stim_manager():
	global STIM_MANAGER

	if STIM_MANAGER == None:
		STIM_MANAGER = pygame.transform.scale(pygame.image.load('sprites/heroes/stim_manager.png'), HEROES_SIZE)
	return STIM_MANAGER

def get_text_background(size=(100*OBJECT_MULTIPLYER_WIDTH, 50*OBJECT_MULTIPLYER_HEIGHT)):
	TEXT_BACKGROUND = pygame.transform.scale(pygame.image.load('sprites/text_background.png'), size)
	return TEXT_BACKGROUND

def get_gray_window(size=SETTINGS_WINDOW_SIZE):
	GRAY_WINDOW = pygame.transform.scale(pygame.image.load('sprites/windows/gray_window.png'), size)
	return GRAY_WINDOW

def get_upgrade_shooter_button_image():
	global UPGRADE_SHOOTER_BUTTON_IMAGE
	if UPGRADE_SHOOTER_BUTTON_IMAGE == None:
		UPGRADE_SHOOTER_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load('sprites/text_background.png'), UPGRADE_SHOOTER_BUTTON_SIZE)
	return UPGRADE_SHOOTER_BUTTON_IMAGE

def get_hero_background():
	global HERO_BACKGROUND
	if HERO_BACKGROUND == None:
		HERO_BACKGROUND = pygame.transform.scale(pygame.image.load('sprites/buttons/hero_button.png'), HEROES_SIZE)
	return HERO_BACKGROUND

def get_field_maradauer():
	global FIELD_MARADAUER_IMAGES
	if FIELD_MARADAUER_IMAGES == None:
		size = (50*OBJECT_MULTIPLYER_WIDTH, 42*OBJECT_MULTIPLYER_HEIGHT)
		shoot_images = [pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_1.png'), size),
						pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_2.png'), size),
						pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_3.png'), size),]
						#pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_4.png'), size),]
		FIELD_MARADAUER_IMAGES = {'stay_image': pygame.transform.scale(pygame.image.load('sprites/marine/marine_stay.png'), FIELDMARADAUER_SIZE), \
								'shoot_image': shoot_images, 'total_size': size}
	return FIELD_MARADAUER_IMAGES

def get_maradauer():
	global MARADAUER_IMAGE
	if MARADAUER_IMAGE == None:
		MARADAUER_IMAGE = pygame.transform.scale(pygame.image.load('sprites/marine/marine_stay.png'), FIELDMARADAUER_SIZE)
	return MARADAUER_IMAGE

def init():
	global HPBAR_IMAGE, MANABAR_IMAGE, MONSTER_IMAGE, HPBAR_BACKGROUND_IMAGE, TOWN_SHOOTER_IMAGES, SETTINGS_BUTTON_IMAGE
	global SETTINGS_WINDOW_IMAGE, TEXT_INPUT_IMAGE, APPLY_SETTINGS_BUTTON, FIGHT_BUTTON, STIM_ON, STIM_OFF
	global STIM_MANAGER, UPGRADE_SHOOTER_BUTTON_IMAGE, HERO_BACKGROUND, MARADAUER_IMAGE, FIELD_MARADAUER_IMAGES

	HPBAR_IMAGE = None
	MANABAR_IMAGE = None
	HPBAR_BACKGROUND_IMAGE = None

	MONSTER_IMAGE = None
	TOWN_SHOOTER_IMAGES = None
	SETTINGS_BUTTON_IMAGE = None
	SETTINGS_WINDOW_IMAGE = None
	TEXT_INPUT_IMAGE = None
	APPLY_SETTINGS_BUTTON = None
	FIGHT_BUTTON = None
	STIM_ON = None
	STIM_OFF = None
	STIM_MANAGER = None
	UPGRADE_SHOOTER_BUTTON_IMAGE = None
	HERO_BACKGROUND = None
	MARADAUER_IMAGE = None
	FIELD_MARADAUER_IMAGES = None

	get_mana_bar()
	get_field_maradauer()
	get_hp_bar()
	get_road()
	get_maradauer()
	get_monster()
	get_castle()
	get_hero_background()
	get_stim_off()
	get_stim_on()
	get_stim_manager()
	get_fight_button()
	get_upgrade_shooter_button_image()
	get_hp_bar_background()
	get_mana_bar_background()
	get_town_shooter()
	get_settings_window()
	get_settings_button()
	get_apply_settings_button()

init()