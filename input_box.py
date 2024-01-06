import pygame as pg
class InputBox:
	def __init__(self, x, y, w, h, txt=''):
		self.rect = pg.Rect(x, y, w, h)
		self.color = pg.Color('dodgerblue')
		self.text = txt
		self.TEXT = pg.font.Font(None, 30).render(self.text, True, self.color)
		self.active = False

	def handle_event(self, event, scrn):
		if event.type == pg.MOUSEBUTTONUP: #the box is clicked
			if self.rect.collidepoint(event.pos): #if click in this btn's bound
				self.active = not self.active
			else:
				self.active = False
		elif event.type == pg.KEYDOWN: #after enter the text
			if self.active:
				if event.key == pg.K_RETURN: #clicked enter btn
					return_value = self.text
					self.active = False
					print(return_value)
					return return_value
				elif event.key == pg.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
				self.TEXT = pg.font.Font(None, 30).render(self.text, True, self.color)		
			else:
				if event.key == pg.K_RETURN:
					return self.text
	def draw(self, scrn):
		pg.draw.rect(scrn, (0,0,0), self.rect, 0) #fill the rect
		scrn.blit(self.TEXT, (self.rect.x+5, self.rect.y+6)) #draw the text
		pg.draw.rect(scrn, self.color, self.rect, 2) #draw the bound
		pg.display.update()
