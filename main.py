from game import Game

class App:
	def __init__(self):
		pass

	def run(self):
		toQuit = False
		while not toQuit:
			self.present_menu()

			game = None
			match input():
				case ['N', 'n']:
					game = self.new_game()
				case ['J', 'j']:
					game = self.join_game()
				case ['Q', 'q']:
					toQuit = True
				case _:
					print('Invalid command')

			if game is None:
				continue

			while not game.is_finish():
				player = game.next_player()
				player.your_turn()
			
			game.present_result()

	def present_menu(self):
		print('Welcome to Gomoku')
		print('(N)ew Game')
		print('(J)oin Game')
		print('(Q)uit Game')

	def new_game(self):
#TODO: initialize a connection host and wait for the other player
		pass

	def join_game(self):
#TODO: initialize a connection from given activation key
		pass

if __name__ == '__main__':
	game = Game([0, 0])

	while not game.is_finish():
		game.present()
		game.next_player()
		game.update(input('Position: '))

	game.present_result()

#	app = App()
#	app.run()
