import images
from constants import *



# Town objects
class Market:
	def __init__(self, place:int):
		self.place = place
		self.location_info = 'Town'
		self.image = images.get_town_market()

		self.rect = self.image.get_rect()

		self.rect.x = WIDTH - TOWN_MARKET_SIZE[0]*self.place - (5*OBJECT_MULTIPLYER_WIDTH*self.place)
		self.rect.y = HEIGHT - 200*OBJECT_MULTIPLYER_HEIGHT

	async def action(self, gf):
		gf.start_trading()