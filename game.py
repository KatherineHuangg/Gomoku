class Game:
	def __init__(self, players):
		self.finished = False
		self.players = players
		self.to_next = False
		self.curr_player = 0
		self.winner = None

		self.board = [[0 for j in range(19)] for i in range(19)]

	def is_finish(self):
		return self.finished

	def next_player(self):
		if self.to_next:
			self.curr_player = (self.curr_player + 1) % 2
			self.to_next = False

		return self.players[self.curr_player]

	def is_in_range(self, pos):
		return pos[0] >= 0 and pos[0] < 19 and pos[1] >= 0 and pos[1] < 19

	def check_finish(self, sym, pos):
		dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
		cnts = [{
			'cont': True,
			'dir': dirs[i],
			'cnt': 0} for i in range(8)]

		for i in range(1, 5):
			true_cnt = 0
			for cnt in cnts:
				if not cnt['cont']:
					continue

				tc = (pos[0] + cnt['dir'][0] * i, pos[1] + cnt['dir'][1] * i)
				if not self.is_in_range(tc):
					cnt['cont'] = False
					continue

				if self.board[tc[0]][tc[1]] == sym:
					cnt['cnt'] += 1
					true_cnt += 1
				else:
					cnt['cont'] = False

			if true_cnt == 0:
				break

		for i in range(0, 8, 2):
			if cnts[i]['cnt'] + cnts[i + 1]['cnt'] >= 4:
				self.winner = self.curr_player
				self.finished = True
				break

	def update(self, move):
		row, col = move[1:], move[:1]
		row = 19 - int(row)
		col = ord(col.upper()) - ord('A')

		if not self.is_in_range((row, col)):
			print('Invalid Input')
			return

		sym = self.curr_player + 1
		self.board[row][col] = sym
		self.check_finish(sym, (row, col))
		self.to_next = True

	def present(self):
		symb = ['.', 'o', 'x']

		print('   ' + ' '.join([chr(ord('A') + i) for i in range(19)]))
		for i, row in enumerate(self.board):
			print('%2d' % (19 - i), end = ' ')
			for col in row:
				print(symb[col], end = ' ')
			print('%2d' % (19 - i))
		print('   ' + ' '.join([chr(ord('A') + i) for i in range(19)]))

	def present_result(self):
		if self.winner is not None:
			print('Winner: Player %d' % (self.winner + 1))
