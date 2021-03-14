# This script load and init images of objects and also their skins, animations and etc.
import pygame
from constants import *

global HPBAR_IMAGE, MANABAR_IMAGE, MONSTER_IMAGE, HPBAR_BACKGROUND_IMAGE, TOWN_SHOOTER_IAMGES, SETTINGS_BUTTON_IMAGE
global SETTINGS_WINDOW_IMAGE, TEXT_INPUT_IMAGE, APPLY_SETTINGS_BUTTON
HPBAR_IMAGE = None
MANABAR_IMAGE = None
HPBAR_BACKGROUND_IMAGE = None

MONSTER_IMAGE = None
TOWN_SHOOTER_IAMGES = None
SETTINGS_BUTTON_IMAGE = None
SETTINGS_WINDOW_IMAGE = None
TEXT_INPUT_IMAGE = None
APPLY_SETTINGS_BUTTON = None


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
	global TOWN_SHOOTER_IAMGES

	if TOWN_SHOOTER_IAMGES == None:
		size = (23*OBJECT_MULTIPLYER_WIDTH, 21*OBJECT_MULTIPLYER_HEIGHT)
		shoot_images = [pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_1.png'), size),
						pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_2.png'), size),
						pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_3.png'), size),]
						#pygame.transform.scale(pygame.image.load('sprites/marine/marine_shoot_4.png'), size),]
		TOWN_SHOOTER_IAMGES = {'stay_image': pygame.transform.scale(pygame.image.load('sprites/marine/marine_stay.png'), TOWN_SHOOTER_SIZE), \
								'shoot_image': shoot_images, 'total_size': size}
	return TOWN_SHOOTER_IAMGES

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