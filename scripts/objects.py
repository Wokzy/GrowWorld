import pygame, images
from constants import *


class Button:
	def __init__(self, name, image, position):
		self.name = name
		self.image = image

		self.rect = image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

	async def action(self, gf):
		if self.name == 'settings_button':
			await gf.open_settings_window()


class Window:
	def __init__(self, name, image, position):
		self.name = name
		self.image = image

		self.rect = image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

		self.mode = False # True or False (hide or show)

	async def action(self, gf):
		pass

class TextInput:
	def __init__(self, name, size, position, text=''):
		self.name = name
		self.image = images.get_text_input(size)

		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

		self.mode = False
		self.text = text

	async def action(self, gf):
		pass

	async def find_index(self, gf):
		for obj in range(len(gf.additional_objects)):
			if gf.additional_objects[obj].name == gf.text_input_obj.name:
				return obj

class Text:
	def __init__(self, name, image, position, text):
		self.name = name
		self.image = image
		self.rect = position
		self.text = text