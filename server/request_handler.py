import socket
import threading
import time
from player import Player
from game import Game
import json


class Server(object):
    PLAYERS = 1

    def __init__(self):
        self.connection_queue = []
        self.game_id = 0
        # server = "188.166.107.89"
        self.addr = ("localhost", 1286)

    def player_thread(self, conn, player):
        """
        Handles communication between clients
        :param conn: connection object
        :param player: Player
        :return: None
        """
        while True:
            try:
                try:
                    data = json.loads(conn.recv(1024).decode())
                except:
                    break

                key = int(list(data.keys())[0])
                send_msg = ""
                if key == -1: # Get game, returns list of players
                    if player.game:
                        send_msg = {
                            player.get_name(): player.get_score() for player in player.game.players
                        }
                    else:
                        send_msg = {}
                if player.game:
                    if key == 0:  # Guess
                        send_msg = player.game.player_guess(player, data['0'][0])
                    elif key == 1:  # Skip
                        send_msg = player.game.skip()
                    elif key == 2:  # Get chat
                        send_msg = player.game.round.chat.get_chat()
                    elif key == 3:  # Get board
                        send_msg = player.game.board.get_board()
                    elif key == 4:  # Get score
                        send_msg = player.game.get_player_scores()
                    elif key == 5:  # Get round
                        send_msg = player.game.round_counter
                    elif key == 6:  # Get word
                        send_msg = player.game.round.word
                    elif key == 7:  # Get skips
                        send_msg = player.game.round.skips
                    elif key == 8:  # Update board
                        player.game.update_board(data['8'][:3])
                    elif key == 9:  # Get round time
                        send_msg = player.game.round.time

                conn.sendall(json.dumps(send_msg).encode()+".".encode())

            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()}: {e}")
                break

        print(f"[DISCONNECTION] {player.name}")
        if player.game:
            player.game.player_disconnected(player)
        if player in self.connection_queue:
            self.connection_queue.remove(player)
        conn.close()

    def handle_queue(self, player):
        """
        Adds given player to queue and starts new game if sufficient number of players
        :param player: Player
        :return: None
        """
        self.connection_queue.append(player)

        if len(self.connection_queue) >= self.PLAYERS:
            game = Game(self.game_id, self.connection_queue[:])
            for p in game.players:
                p.set_game(game)
            self.game_id += 1
            self.connection_queue = []

    def authentication(self, conn, addr):
        """
        Authentication here
        :param conn: connection object
        :param addr: str
        :return: None
        """
        try:
            name = conn.recv(1024).decode()
            if not name:
                raise Exception("No name received")
            conn.sendall("[CONNECTED]".encode())

            player = Player(addr, name)
            self.handle_queue(player)
            threading.Thread(target=self.player_thread, args=(conn, player)).start()
        except Exception as e:
            print(f"[EXCEPTION] {e}")
            conn.close()

    def connected_thread(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(self.addr)
        except socket.error as e:
            print(f"[SOCKET ERROR] {e}")

        sock.listen(1)
        print("[START] Waiting for a connection")

        while True:
            conn, addr = sock.accept()
            print(f"[CONNECT] {addr[0]}:{addr[1]}")
            self.authentication(conn, addr)


if __name__ == "__main__":
    s = Server()
    # threading.Thread(target=s.connected_thread).start()
    s.connected_thread()