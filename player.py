import sys,time
class Player:
    def __init__(self, conn):
        self.conn = conn

    def your_turn():
        print("It's your turn now.")

    def join_game(self, game):
        self.game = game

class LocalPlayer(Player):
    def __init__(self, conn):
        super(LocalPlayer, self).__init__(conn)

    def your_turn(self): 
        send_msg = input('It is your turn: ')
        self.game.update(send_msg)
        self.conn.send(send_msg.encode())

class SyncPlayer(Player):
    def __init__(self, conn):
        super(SyncPlayer, self).__init__(conn)
        
    def your_turn(self):
        print('Waiting for the other player ...')
        recv_msg = self.conn.recv(1024)
        recv_msg = recv_msg.decode()
        self.game.update(recv_msg)
