import sys,time
class Player:
    def __init__(self, conn, presenter):
        self.conn = conn
        self.presenter = presenter

    def join_game(self, game, side):
        self.game = game

class LocalPlayer(Player):
    def __init__(self, conn, presenter):
        super(LocalPlayer, self).__init__(conn, presenter)

    def join_game(self, game, side):
        super(LocalPlayer, self).join_game(game, side)
        self.presenter.set_self_side(side)

    def your_turn(self): 
        while True:
            send_msg = self.presenter.ask_for_cell_input()
            if self.game.update(send_msg):
                self.conn.send(send_msg.encode())
                break

class SyncPlayer(Player):
    def __init__(self, conn, presenter):
        super(SyncPlayer, self).__init__(conn, presenter)
        self.conn.setblocking(False)
        
    def your_turn(self):
        self.presenter.hold('Wait for the opponent ...')
        while True:
            try:
                recv_msg = self.conn.recv(1024)
                recv_msg = recv_msg.decode()
                self.game.update(recv_msg)
                break
            except:
                self.presenter.update()

        self.presenter.unhold()
        self.presenter.update()
