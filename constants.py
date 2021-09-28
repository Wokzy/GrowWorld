# Constants of the game
import pickle, pygame

try:
	with open('config.bin', 'rb') as f:
		data = pickle.load(f)
		WIDTH = data['width']
		HEIGHT = data['height']
	#WIDTH = 1280
	#HEIGHT = 720
except Exception as e:
	WIDTH = 1280
	HEIGHT = 720
	print('config loading error, setting to defaults (1280, 720)')
	print(e)

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 360

FPS = 60

OBJECT_MULTIPLYER_WIDTH = WIDTH // DEFAULT_WIDTH
OBJECT_MULTIPLYER_HEIGHT = HEIGHT // DEFAULT_HEIGHT
AVERAGE_MULTIPLYER = (OBJECT_MULTIPLYER_WIDTH+OBJECT_MULTIPLYER_HEIGHT)//2

WINDOW_RESOLUTION = (WIDTH, HEIGHT)

DEFAULT_CASTLE_WIDTH = 200
DEFAULT_CASTLE_HEIGHT = 220
CASTLE_SIZE = (DEFAULT_CASTLE_WIDTH*OBJECT_MULTIPLYER_WIDTH, DEFAULT_CASTLE_HEIGHT*OBJECT_MULTIPLYER_HEIGHT)

DEFAULT_ROAD_WIDTH = DEFAULT_WIDTH
DEFAULT_ROAD_HEIGHT = 247 #DEFAULT_HEIGHT // 2 + 80
ROAD_SIZE = (DEFAULT_ROAD_WIDTH*OBJECT_MULTIPLYER_WIDTH, DEFAULT_ROAD_HEIGHT*OBJECT_MULTIPLYER_HEIGHT)

DEFAULT_HPBAR_WIDTH = 180
DEFAULT_HPBAR_HEIGHT = 15
DEFAULT_HPBAR_SIZE = (DEFAULT_HPBAR_WIDTH*OBJECT_MULTIPLYER_WIDTH, DEFAULT_HPBAR_HEIGHT*OBJECT_MULTIPLYER_HEIGHT)
HPBAR_BACKGROUND_SIZE = DEFAULT_HPBAR_SIZE

DEFAULT_MANABAR_WIDTH = 180
DEFAULT_MANABAR_HEIGHT = 15
DEFAULT_MANABAR_SIZE = (DEFAULT_MANABAR_WIDTH*OBJECT_MULTIPLYER_WIDTH, DEFAULT_MANABAR_HEIGHT*OBJECT_MULTIPLYER_HEIGHT)
MANABAR_BACKGROUND_SIZE = DEFAULT_MANABAR_SIZE

DEFAULT_INFO_FONT_SIZE = 10
INFO_FONT_SIZE = DEFAULT_INFO_FONT_SIZE*AVERAGE_MULTIPLYER

DEFAULT_MONSTER_SIZE = (50, 50)
MONSTER_SIZE = (DEFAULT_MONSTER_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_MONSTER_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)

MANA_ADD_TIMER = FPS * 0.05

DEFAULT_TOWN_SHOOTER_SIZE = (14, 21)
TOWN_SHOOTER_SIZE = (DEFAULT_TOWN_SHOOTER_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_TOWN_SHOOTER_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)

DEFAULT_SETTINGS_BUTTON_SZIE = (25, 25)
SETTINGS_BUTTON_SIZE = (DEFAULT_SETTINGS_BUTTON_SZIE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_SETTINGS_BUTTON_SZIE[1]*OBJECT_MULTIPLYER_HEIGHT)

DEFAULT_SETTINGS_WINDOW_SIZE = (200, 285)
SETTINGS_WINDOW_SIZE = (DEFAULT_SETTINGS_WINDOW_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_SETTINGS_WINDOW_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)

DEFAULT_APPLY_SETTIGS_BUTTON_SIZE = (120, 50)
APPLY_SETTIGS_BUTTON_SIZE = (DEFAULT_APPLY_SETTIGS_BUTTON_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_APPLY_SETTIGS_BUTTON_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)

NUMBERS_KEYS = '123456789'#[pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]

DEFAULT_FIGHT_BUTTON_SIZE = (128, 64)
FIGHT_BUTTON_SIZE = (DEFAULT_FIGHT_BUTTON_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_FIGHT_BUTTON_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)

STIMPACK_BUFF = 0.6
DEFAULT_STIM_ON_SIZE = (7, 10)
STIM_ON_SIZE = (DEFAULT_STIM_ON_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_STIM_ON_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)
DEFAULT_STIM_OFF_SIZE = (7, 10)
STIM_OFF_SIZE = (DEFAULT_STIM_OFF_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_STIM_OFF_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)

DEFAULT_HEROES_SIZE = (40, 40)
HEROES_SIZE = (DEFAULT_HEROES_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_HEROES_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)

DEFAULT_UPGRADE_SHOOTER_BUTTON_SIZE = (100, 25)
UPGRADE_SHOOTER_BUTTON_SIZE = (DEFAULT_UPGRADE_SHOOTER_BUTTON_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_UPGRADE_SHOOTER_BUTTON_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)

DEFAULT_FIELDMARADAUER_SIZE = (30, 42)
FIELDMARADAUER_SIZE = (DEFAULT_FIELDMARADAUER_SIZE[0]*OBJECT_MULTIPLYER_WIDTH, DEFAULT_FIELDMARADAUER_SIZE[1]*OBJECT_MULTIPLYER_HEIGHT)

CLOSE_BUTTON_SIZE = (25*OBJECT_MULTIPLYER_WIDTH, 25*OBJECT_MULTIPLYER_HEIGHT)

TAKE_OFF_BUTTON_SIZE = (128*OBJECT_MULTIPLYER_WIDTH, 64*OBJECT_MULTIPLYER_HEIGHT)
EQUIP_BUTTON_SIZE = (128*OBJECT_MULTIPLYER_WIDTH, 64*OBJECT_MULTIPLYER_HEIGHT)

GOLD_COLOUR = (240, 236, 55)

TOWN_MARKET_SIZE = (64*OBJECT_MULTIPLYER_WIDTH, 64*OBJECT_MULTIPLYER_HEIGHT)

MOVE_GLOBAL_LOCATION_BUTTON_SIZE = (90*OBJECT_MULTIPLYER_WIDTH, 40*OBJECT_MULTIPLYER_HEIGHT)

BUY_BUTTON_SIZE = (120*OBJECT_MULTIPLYER_WIDTH, 70*OBJECT_MULTIPLYER_HEIGHT)
SELL_BUTTON_SIZE = (120*OBJECT_MULTIPLYER_WIDTH, 70*OBJECT_MULTIPLYER_HEIGHT)

TRAIDING_RAISE_SIZE = (45*OBJECT_MULTIPLYER_WIDTH, 26*OBJECT_MULTIPLYER_HEIGHT)
TRAIDING_MINUS_SIZE = (45*OBJECT_MULTIPLYER_WIDTH, 26*OBJECT_MULTIPLYER_HEIGHT)
TRAIDING_FALL_SIZE = (45*OBJECT_MULTIPLYER_WIDTH, 26*OBJECT_MULTIPLYER_HEIGHT)

REMOVE_DATA_SIZE = (170*OBJECT_MULTIPLYER_WIDTH, 70*OBJECT_MULTIPLYER_HEIGHT)

YES_BUTTON_SIZE = (170*OBJECT_MULTIPLYER_WIDTH, 70*OBJECT_MULTIPLYER_HEIGHT)
NO_BUTTON_SIZE = (170*OBJECT_MULTIPLYER_WIDTH, 70*OBJECT_MULTIPLYER_HEIGHT)

BLEW_SIZE = ROCKETBOOM_SIZE = (50*OBJECT_MULTIPLYER_WIDTH, 50*OBJECT_MULTIPLYER_HEIGHT)

RANGE_MONSTER_SIZE = (31*OBJECT_MULTIPLYER_WIDTH, 39*OBJECT_MULTIPLYER_HEIGHT)
SKILLS_BUTTON_SIZE = (60*OBJECT_MULTIPLYER_WIDTH, 60*OBJECT_MULTIPLYER_HEIGHT)
BONUS_GOLD_SKILL_BUTTON_SIZE = (40*OBJECT_MULTIPLYER_WIDTH, 40*OBJECT_MULTIPLYER_HEIGHT)
CRITICAL_SHOT_SKILL_BUTTON_SIZE = (40*OBJECT_MULTIPLYER_WIDTH, 40*OBJECT_MULTIPLYER_HEIGHT)

UPGRADE_BUTTON_SIZE = (64*OBJECT_MULTIPLYER_WIDTH, 20*OBJECT_MULTIPLYER_HEIGHT)

TOXIC_BULLET_SIZE = (26*OBJECT_MULTIPLYER_WIDTH, 11*OBJECT_MULTIPLYER_HEIGHT)

RANGE_MONSTER_ATTACK_SIZE = (45*OBJECT_MULTIPLYER_WIDTH, 39*OBJECT_MULTIPLYER_HEIGHT)