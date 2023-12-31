import pygame as pg
import numpy as np

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

		self.side = None
		self.board = None
		self.stay = None
		self.clock = pg.time.Clock()

		pg.init()
		self.scrn = pg.display.set_mode(self.wsize)

	def set_self_side(self, side):
		self.side = side
		
	def present_title(self, title):
		print(title)

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
		self.board = board.copy()
		self.update()

	def present_end_result(self, res_msg):
		print(res_msg)

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
