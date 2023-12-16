from game import Game
import socket
from player import *

class App:
	def __init__(self):
		pass

	def run(self):
		toQuit = False
		while not toQuit:
			self.present_menu()

			game = None
			match input('Choose action: '):
				case 'N' | 'n':
					game = self.new_game()
				case 'J' | 'j':
					game = self.join_game()
				case 'Q' | 'q':
					toQuit = True
				case _:
					print('Invalid command')

			if game is None:
				continue

			while not game.is_finish():
				game.present()
				player = game.next_player()
				player.your_turn()
			
			game.present()
			game.present_result()

	def present_menu(self):
		print('Welcome to Gomoku')
		print('(N)ew Game')
		print('(J)oin Game')
		print('(Q)uit Game')

	def new_game(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('8.8.8.8', 53))
		self_ip = s.getsockname()[0]

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self_ip, 0))
		s.listen(1)

		print(self_ip, s.getsockname()[1])

		conn, addr = s.accept()
		player1 = LocalPlayer(conn)
		player2 = SyncPlayer(conn)
		return Game([player1,player2])

	def join_game(self):
#TODO: initialize a connection from given activation key
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		ip = input('Remote IP address: ')
		port = input('Remote port: ')
		s.connect((ip, int(port)))

		player1 = SyncPlayer(s)
		player2 = LocalPlayer(s)
		return Game([player1,player2])

if __name__ == '__main__':
	'''game = Game([0, 0])

	while not game.is_finish():
		game.present()
		game.next_player()
		game.update(input('Position: '))

	game.present_result()'''

	app = App()
	app.run()
