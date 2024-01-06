import pygame as pg
import numpy as np
from button import Button
from input_box import InputBox

class CLI:
	def present_title(self, title):
		print(title)

	def set_self_side(self, side):
		pass

	def present_menu_and_wait(self, choices, prompt):
		targets = {}
		for i, ch in enumerate(choices):
			key = ch[0].upper()
			targets[key] = i
			print('(%s)%s' % (key, ch[1:]))

		cmd = input(prompt).upper()
		if cmd not in targets:
			return -1
		return targets[cmd]

	def present_conn_info(self, ip, port):
		print(ip, port)

	def ask_for_conn_info(self):
		ip = input('Remote IP: ')
		port = input('Remote port: ')

		return (ip, port)

	def present_board(self, board):
		symb = ['.', 'o', 'x']

		print('   ' + ' '.join([chr(ord('A') + i) for i in range(19)]))
		for i, row in enumerate(board):
			print('%2d' % (19 - i), end = ' ')
			for col in row:
				print(symb[col], end = ' ')
			print('%2d' % (19 - i))
		print('   ' + ' '.join([chr(ord('A') + i) for i in range(19)]))

	def present_end_result(self, res_msg):
		print(res_msg)

	def ask_for_cell_input(self):
		return input('Your turn: ')

	def hold(self, prompt):
		print(prompt)

	def unhold(self):
		pass

	def present_error(self, err):
		print(err)

	def update(self):
		pass

class GUI:
	def __init__(self):
		self.wsize = np.array([720, 720])
		self.csize = 32
		self.bsize = np.array([19, 19]) * self.csize
		self.bori = (self.wsize - self.bsize) / 2

		self.reset()

		self.img_paths = ['assets/new_game.png', 'assets/join_game.png', 'assets/quit.png']
		self.btns = []

		#new

		pg.init()	
		self.font = pg.font.SysFont("arial", 30)
		self.scrn = pg.display.set_mode(self.wsize)

	def reset(self):
		self.side = None
		self.board = None
		self.stay = None
		self.clock = pg.time.Clock()

		#new

	def set_self_side(self, side):
		self.side = side
		
	def present_title(self, title):
		pg.display.set_caption(title)
		print(title)

	def present_menu_and_wait(self, choices, prompt):
		#new
		while True:
			self.scrn.fill((0, 0, 0))
			MENU_TEXT = self.font.render(prompt, True, (255,255,255),(0,0,0))
			MENU_RECT = MENU_TEXT.get_rect(center=(360, 100))
			self.scrn.blit(MENU_TEXT,MENU_RECT)			

			pg.display.flip()
			self.clock.tick(60)
						
			targets = {}
			for i, ch in enumerate(choices):
				key = ch[0].upper()
				targets[key] = i
				print('(%s)%s' % (key, ch[1:]))			
			
			###Draw buttons
			interval = 20 #interval between 2 btns
			y = 100
			for path in self.img_paths:
				btn = Button(path, y)
				self.btns.append(btn)
				y += btn.img.get_height() + interval
			
			for btn in self.btns:
				btn.draw(self.scrn)
			pg.display.update()
				
			###Check if button is clicked
			while True:
				for evnt in pg.event.get():
					if evnt.type == pg.MOUSEBUTTONUP:
						mos_pos = pg.mouse.get_pos()
						for i, btn in enumerate(self.btns):
							if btn.in_bound(mos_pos):
								print(f"Button {i+1} clicked")
								return i
			'''
			cmd = input(prompt).upper()
			if cmd not in targets:
				return -1		
			print(targets[cmd])
			return targets[cmd]
			'''
	def present_conn_info(self, ip, port):
		print(ip, port)
		info = "Your IP is " + str(ip) + ", and port is " + str(port)
		MENU_TEXT = self.font.render(info, True, (255,255,255),(0,0,0))
		MENU_RECT = MENU_TEXT.get_rect(center=(360, 550))
		self.scrn.blit(MENU_TEXT,MENU_RECT)
		pg.display.update()	
	
	def ask_for_conn_info(self):
		input_ip = InputBox(280, 550, 200, 32)
		input_port = InputBox(280, 600, 200, 32)
		input_boxes = [input_ip, input_port]		
		ip_label = self.font.render(" Remote IP :", True, (255,255,255),(0,0,0))
		port_label = self.font.render("Remote Port:", True, (255,255,255),(0,0,0))
		
		run = True
		result = ['','']
		while run:
			for evnt in pg.event.get():
				result[0] = input_ip.handle_event(evnt, self.scrn)
				result[1] = input_port.handle_event(evnt, self.scrn)
					
				if result[0] is not None or result[1] is not None:
					if input_boxes[0].text and input_boxes[1].text:
						input_boxes[0].text, input_boxes[1].text = '',''	
						run = False	
			self.scrn.blit(ip_label, (60, input_ip.rect.y ))
			self.scrn.blit(port_label, (60, input_port.rect.y))
			for input_box in input_boxes:
				input_box.draw(self.scrn)
		print(result)	
		return (result)

	def present_board(self, board):
		self.board = board.copy()
		self.update()

	def present_end_result(self, res_msg):
		print(res_msg)
		TEXT = self.font.render(res_msg, True, (255,255,255),(0,0,0))
		RECT = TEXT.get_rect(center=(360, 600))
		
		run = True
		while run:
			for evnt in pg.event.get():
				if evnt.type == pg.KEYDOWN:			
					self.scrn.blit(TEXT,RECT)
					run = False
			self.scrn.blit(TEXT, RECT)
			pg.display.update()			

	def ask_for_cell_input(self):
		cont = True
		while cont:
			for evnt in pg.event.get():
				if evnt.type == pg.MOUSEMOTION:
					mos_pos = pg.mouse.get_pos()
					if not self.is_on_board(mos_pos):
						self.stay = None
						continue
					self.stay = self.pos_to_cell(mos_pos)
				elif evnt.type == pg.MOUSEBUTTONUP:
					if self.stay is not None:
						cont = False

			self.update()

		return '%s%d' % (chr(ord('A') + int(self.stay[0])), 19 - int(self.stay[1]))

	def hold(self, prompt):		
		print(prompt)
		
	def unhold(self):
		pass

	def present_error(self, err):
		print(err)

	def update(self):
		for evnt in pg.event.get():
			if evnt.type == pg.QUIT:
				pg.quit()
				return

		self.scrn.fill("black")

		pg.draw.rect(self.scrn, '#da6d42', pg.Rect(self.bori, self.bsize))
		for i in range(19):
			st = self.get_cell_center((0, i))
			ed = self.get_cell_center((18, i))
			pg.draw.line(self.scrn, (0, 0, 0), st, ed)

			st = self.get_cell_center((i, 0))
			ed = self.get_cell_center((i, 18))
			pg.draw.line(self.scrn, (0, 0, 0), st, ed)

		for i in range(3, 19, 6):
			for j in range(3, 19, 6):
				pg.draw.circle(self.scrn, (0, 0, 0), self.get_cell_center((i, j)), 8)

		color = [None, (0, 0, 0), (255, 255, 255)]
		if self.board is not None:
			for i, row in enumerate(self.board):
				for j, ele in enumerate(row):
					if int(ele) == 0:
						continue

					pg.draw.circle(self.scrn, color[ele], self.get_cell_center((j, i)), 15)

		if self.stay is not None:
			pg.draw.circle(self.scrn, color[self.side], self.get_cell_center(self.stay), 15)

		pg.display.flip()
		self.clock.tick(60)

	def poll_input(self):
		for evnt in pg.event.get():
			if evnt.type == pg.QUIT:
				pg.quit()
				return


	def get_cell_center(self, pos):
		pos = np.array(pos, dtype = np.float32)
		offset = np.array([0.5, 0.5], dtype = np.float32)
		return self.bori + (pos + offset) * self.csize

	def is_on_board(self, pos):
		pos -= self.bori

		x_on = pos[0] > 0 and pos[0] < self.bsize[0]
		y_on = pos[1] > 0 and pos[1] < self.bsize[1]

		return x_on and y_on

	def pos_to_cell(self, pos):
		pos -= self.bori
		pos //= self.csize

		return pos
