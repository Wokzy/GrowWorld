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

def get_rocket_man():
	global ROCKET_MAN
	if ROCKET_MAN == None:
		ROCKET_MAN = pygame.transform.scale(pygame.image.load('sprites/heroes/rocket_man.png'), HEROES_SIZE)
	return ROCKET_MAN

def get_rocket_boom():
	global BLEW_IMAGES
	if BLEW_IMAGES == None:
		BLEW_IMAGES = [pygame.transform.scale(pygame.image.load('sprites/images/blew_animation/Sprite-0001.png'), BLEW_SIZE), pygame.transform.scale(pygame.image.load('sprites/images/blew_animation/Sprite-0002.png'), BLEW_SIZE), pygame.transform.scale(pygame.image.load('sprites/images/blew_animation/Sprite-0003.png'), BLEW_SIZE), pygame.transform.scale(pygame.image.load('sprites/images/blew_animation/Sprite-0004.png'), BLEW_SIZE)]
	return BLEW_IMAGES

def get_monster():
	global MONSTER_IMAGE
	return MONSTER_IMAGE

def get_range_monster():
	global RANGE_MONSTER_IMAGES

	if RANGE_MONSTER_IMAGES == None:
		size = RANGE_MONSTER_SIZE
		RANGE_MONSTER_IMAGES = {'stay_image':pygame.transform.scale(pygame.image.load('sprites/enemyes/range_monster_stay_image.png'), size),
								'attack_image':pygame.transform.scale(pygame.image.load('sprites/enemyes/range_monster_attack_image.png'), RANGE_MONSTER_ATTACK_SIZE),
								'move_images':[pygame.transform.scale(pygame.image.load('sprites/enemyes/range_monster_move_image_1.png'), size), pygame.transform.scale(pygame.image.load('sprites/enemyes/range_monster_move_image_2.png'), size)]
								}

	return RANGE_MONSTER_IMAGES

def get_toxic_bullet():
	global TOXIC_BULLET

	if TOXIC_BULLET == None:
		TOXIC_BULLET = [pygame.transform.scale(pygame.image.load('sprites/bullets/toxic_bullet_1.png'), TOXIC_BULLET_SIZE), pygame.transform.scale(pygame.image.load('sprites/bullets/toxic_bullet_2.png'), TOXIC_BULLET_SIZE)]

	return TOXIC_BULLET

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
	return SETTINGS_BUTTON_IMAGE

def get_settings_window():
	global SETTINGS_WINDOW_IMAGE
	return SETTINGS_WINDOW_IMAGE

def get_text_input(size):
	global TEXT_INPUT_IMAGE
	TEXT_INPUT_IMAGE = pygame.transform.scale(pygame.image.load('sprites/text_input.png'), size)
	return TEXT_INPUT_IMAGE

def get_apply_settings_button():
	global APPLY_SETTINGS_BUTTON
	return APPLY_SETTINGS_BUTTON

def get_fight_button():
	global FIGHT_BUTTON
	return FIGHT_BUTTON

def get_stim_on():
	global STIM_ON
	return STIM_ON

def get_stim_off():
	global STIM_OFF
	return STIM_OFF

def get_stim_manager():
	global STIM_MANAGER
	return STIM_MANAGER

def get_text_background(size=(100*OBJECT_MULTIPLYER_WIDTH, 50*OBJECT_MULTIPLYER_HEIGHT)):
	TEXT_BACKGROUND = pygame.transform.scale(pygame.image.load('sprites/text_background.png'), size)
	return TEXT_BACKGROUND

def get_gray_window(size=SETTINGS_WINDOW_SIZE):
	GRAY_WINDOW = pygame.transform.scale(pygame.image.load('sprites/windows/gray_window.png'), size)
	return GRAY_WINDOW

def get_upgrade_shooter_button_image():
	global UPGRADE_SHOOTER_BUTTON_IMAGE
	return UPGRADE_SHOOTER_BUTTON_IMAGE

def get_hero_background():
	global HERO_BACKGROUND
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
	return MARADAUER_IMAGE

def get_close_button():
	global CLOSE_BUTTON
	return CLOSE_BUTTON

def get_take_off_button():
	global TAKE_OFF_BUTTON
	return TAKE_OFF_BUTTON

def get_equip_button():
	global EQUIP_BUTTON
	return EQUIP_BUTTON

def get_unit_healer():
	global UNIT_HEALER
	return UNIT_HEALER

def get_crystal(size=(5, 5)):
	return pygame.transform.scale(pygame.image.load('sprites/crystal.png'), size)

def get_town_market():
	global TOWN_MARKET
	return TOWN_MARKET

def get_goto_town_button():
	global GOTO_TOWN
	return GOTO_TOWN

def get_goto_castle_button():
	global GOTO_CASTLE
	return GOTO_CASTLE

def get_buy_button():
	global BUY_BUTTON
	return BUY_BUTTON

def get_sell_button():
	global SELL_BUTTON
	return SELL_BUTTON

def get_trading_raise():
	global TRAIDING_RAISE
	return TRAIDING_RAISE

def get_trading_minus():
	global TRAIDING_MINUS
	return TRAIDING_MINUS

def get_trading_fall():
	global TRAIDING_FALL
	return TRAIDING_FALL

def get_remove_data():
	global REMOVE_DATA
	return REMOVE_DATA

def get_yes_button():
	global YES_BUTTON
	return YES_BUTTON

def get_no_button():
	global NO_BUTTON
	return NO_BUTTON

def get_skills_button():
	global SKILLS_BUTTON
	return SKILLS_BUTTON

def get_bonus_gold_skill_button():
	global BONUS_GOLD_SKILL_BUTTON
	return BONUS_GOLD_SKILL_BUTTON

def get_critical_shot_skill_button():
	global CRITICAL_SHOT_SKILL_BUTTON
	return CRITICAL_SHOT_SKILL_BUTTON

def init():
	global HPBAR_IMAGE, MANABAR_IMAGE, MONSTER_IMAGE, HPBAR_BACKGROUND_IMAGE, TOWN_SHOOTER_IMAGES, SETTINGS_BUTTON_IMAGE
	global SETTINGS_WINDOW_IMAGE, TEXT_INPUT_IMAGE, APPLY_SETTINGS_BUTTON, FIGHT_BUTTON, STIM_ON, STIM_OFF
	global STIM_MANAGER, UPGRADE_SHOOTER_BUTTON_IMAGE, HERO_BACKGROUND, MARADAUER_IMAGE, FIELD_MARADAUER_IMAGES
	global CLOSE_BUTTON, TAKE_OFF_BUTTON, EQUIP_BUTTON, UNIT_HEALER, TOWN_MARKET, GOTO_TOWN, GOTO_CASTLE, SELL_BUTTON
	global BUY_BUTTON, TRAIDING_FALL, TRAIDING_MINUS, TRAIDING_RAISE, REMOVE_DATA, NO_BUTTON, YES_BUTTON
	global BLEW_IMAGES, ROCKET_MAN, SKILLS_BUTTON, BONUS_GOLD_SKILL_BUTTON, RANGE_MONSTER_IMAGES, TOXIC_BULLET
	global CRITICAL_SHOT_SKILL_BUTTON

	HPBAR_IMAGE = None
	MANABAR_IMAGE = None
	HPBAR_BACKGROUND_IMAGE = None

	MONSTER_IMAGE = pygame.transform.scale(pygame.image.load('sprites/enemyes/monster.png'), MONSTER_SIZE)
	TOWN_SHOOTER_IMAGES = None
	SETTINGS_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load('sprites/buttons/gear.png'), SETTINGS_BUTTON_SIZE)
	SETTINGS_WINDOW_IMAGE = pygame.transform.scale(pygame.image.load('sprites/windows/settings_window.png'), SETTINGS_WINDOW_SIZE)
	TEXT_INPUT_IMAGE = None
	APPLY_SETTINGS_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/apply.png'), APPLY_SETTIGS_BUTTON_SIZE)
	FIGHT_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/fight.png'), FIGHT_BUTTON_SIZE)
	STIM_ON = pygame.transform.scale(pygame.image.load('sprites/flags/stim_on.png'), STIM_ON_SIZE)
	STIM_OFF = pygame.transform.scale(pygame.image.load('sprites/flags/stim_off.png'), STIM_OFF_SIZE)
	STIM_MANAGER = pygame.transform.scale(pygame.image.load('sprites/heroes/stim_manager.png'), HEROES_SIZE)
	UPGRADE_SHOOTER_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load('sprites/text_background.png'), UPGRADE_SHOOTER_BUTTON_SIZE)
	HERO_BACKGROUND = pygame.transform.scale(pygame.image.load('sprites/buttons/hero_button.png'), HEROES_SIZE)
	MARADAUER_IMAGE = pygame.transform.scale(pygame.image.load('sprites/marine/marine_stay.png'), FIELDMARADAUER_SIZE)
	FIELD_MARADAUER_IMAGES = None
	CLOSE_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/close_button.png'), CLOSE_BUTTON_SIZE)
	TAKE_OFF_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/take_off.png'), TAKE_OFF_BUTTON_SIZE)
	EQUIP_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/equip.png'), EQUIP_BUTTON_SIZE)
	UNIT_HEALER = pygame.transform.scale(pygame.image.load('sprites/heroes/unit_healer.png'), HEROES_SIZE)
	TOWN_MARKET = pygame.transform.scale(pygame.image.load('sprites/ground_objects/market.png'), TOWN_MARKET_SIZE) #'sprites/ground_objects/market.png'
	GOTO_TOWN = pygame.transform.scale(pygame.image.load('sprites/buttons/goto_town.png'), MOVE_GLOBAL_LOCATION_BUTTON_SIZE)
	GOTO_CASTLE = pygame.transform.scale(pygame.image.load('sprites/buttons/goto_castle.png'), MOVE_GLOBAL_LOCATION_BUTTON_SIZE)
	BUY_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/Buy.png'), BUY_BUTTON_SIZE)
	SELL_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/Sell.png'), SELL_BUTTON_SIZE)
	TRAIDING_RAISE = pygame.transform.scale(pygame.image.load('sprites/images/traiding_raise.png'), TRAIDING_RAISE_SIZE)
	TRAIDING_FALL = pygame.transform.scale(pygame.image.load('sprites/images/traiding_fall.png'), TRAIDING_FALL_SIZE)
	TRAIDING_MINUS = pygame.transform.scale(pygame.image.load('sprites/images/traiding_minus.png'), TRAIDING_MINUS_SIZE)
	REMOVE_DATA = pygame.transform.scale(pygame.image.load('sprites/buttons/Remove_data.png'), REMOVE_DATA_SIZE)
	NO_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/No_green.png'), NO_BUTTON_SIZE)
	YES_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/Yes_red.png'), YES_BUTTON_SIZE)
	BLEW_IMAGES = None
	ROCKET_MAN = None
	SKILLS_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/skills_button.png'), SKILLS_BUTTON_SIZE)#pygame.transform.scale(pygame.image.load('sprites/buttons/skills_button.png'), SKILLS_BUTTON_SIZE)
	BONUS_GOLD_SKILL_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/bonus_gold_skill.png'), BONUS_GOLD_SKILL_BUTTON_SIZE)#pygame.transform.scale(pygame.image.load('sprites/buttons/bonus_gold_skill_button.png'), BONUS_GOLD_SKILL_BUTTON_SIZE)
	CRITICAL_SHOT_SKILL_BUTTON = pygame.transform.scale(pygame.image.load('sprites/buttons/critical_shot.png'), CRITICAL_SHOT_SKILL_BUTTON_SIZE)
	RANGE_MONSTER_IMAGES = None
	TOXIC_BULLET = None

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
	get_close_button()
	get_take_off_button()
	get_equip_button()
	get_unit_healer()
	get_town_market()
	get_goto_town_button()
	get_goto_castle_button()
	get_sell_button()
	get_buy_button()
	get_trading_minus()
	get_trading_fall()
	get_trading_raise()
	get_remove_data()
	get_yes_button()
	get_no_button()
	get_rocket_boom()
	get_rocket_man()
	get_range_monster()
	get_toxic_bullet()

init()