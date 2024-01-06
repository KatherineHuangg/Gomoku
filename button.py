import pygame as pg
class Button:
	def __init__(self, img_path, offset_y):
		self.img = pg.image.load(img_path)
		
		self.img_size = (200, 100)
		self.img = pg.transform.scale(self.img, self.img_size)
		self.rect = self.img.get_rect()
		self.rect.center = (360, 100 + offset_y)
	
	def draw(self, scrn):
		scrn.blit(self.img, self.rect)		

	def in_bound(self, pos):
		return self.rect.collidepoint(pos)	
