from game import Game
from ui import CLI, GUI
import socket
import select
from player import *

class App:
	def __init__(self, ui):
		self.ui = ui

	def run(self):
		toQuit = False
		while not toQuit:
			self.ui.present_title('Welcome to Gomoku')

			game = None
			menu = [
				'New Game',
				'Join Game',
				'Quit',
			]
			match self.ui.present_menu_and_wait(menu, 'Choose action: '):
				case 0:
					game = self.new_game()
				case 1:
					game = self.join_game()
				###new
				case 2:
					toQuit = True
					break
				case _:
					self.ui.present_error('Invalid command')
					continue

			while not game.is_finish():
				game.present()
				player = game.next_player()
				player.your_turn()
			
			game.present()
			game.present_result()

			self.ui.reset()

	def new_game(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('8.8.8.8', 53))
		self_ip = s.getsockname()[0]

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self_ip, 0))
		s.listen(1)

		self.ui.present_conn_info(self_ip, s.getsockname()[1])

		self.ui.hold('Wait for opponent to join...')
		
		rl = [s]
		done = False
		while not done:
			r, _, _ = select.select(rl, [], [], 0.01)
			for rb in r:
				if rb is s:
					conn, addr = s.accept()
					done = True
			self.ui.poll_input()
		self.ui.unhold()

		player1 = LocalPlayer(conn, self.ui)
		player2 = SyncPlayer(conn, self.ui)
		return Game([player1,player2], self.ui)

	def join_game(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		ip, port = self.ui.ask_for_conn_info()
		s.connect((ip, int(port)))

		player1 = SyncPlayer(s, self.ui)
		player2 = LocalPlayer(s, self.ui)
		return Game([player1,player2], self.ui)

if __name__ == '__main__':
	app = App(GUI())
	app.run()
