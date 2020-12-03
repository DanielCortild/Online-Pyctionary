import socket
import threading
import time
from player import Player
from game import Game
import json


class Server(object):
    PLAYERS = 2

    def __init__(self):
        self.connection_queue = []
        self.game_id = 0

    def player_thread(self, conn, player):
        """
        Handles communication between clients
        :param conn: connection object
        :param ip: str
        :param name: str
        :return: None
        """
        while True:
            try:
                try:
                    data = conn.recv(1024)
                    data = json.loads(data.decode())
                    print(f"[LOG] Received Value : {data}")
                except Exception as e:
                    break

                keys = [int(key) for key in data.keys()]
                send_msg = {key: [] for key in keys}

                for key in keys:
                    if key == -1: # Get game, returns list of players
                        if player.game:
                            send = {player.get_name(): player.get_score() for player in player.game.players}
                            send_msg[-1] = send
                        else:
                            send_msg[-1] = []
                    if player.game:
                        if key == 0:  # Guess
                            correct = player.game.player_guess(player, data['0'][0])
                            send_msg[0] = correct
                        elif key == 1:  # Skip
                            skip = player.game.skip()
                            send_msg[1] = skip
                        elif key == 2:  # Get chat
                            content = player.game.round.chat.get_chat()
                            send_msg[2] = content
                        elif key == 3:  # Get board
                            brd = player.game.board.get_board()
                            send_msg[3] = brd
                        elif key == 4:  # Get score
                            scores = player.game.get_player_scores()
                            send_msg[4] = scores
                        elif key == 5:  # Get round
                            rnd = player.game.round_counter
                            send_msg[5] = rnd
                        elif key == 6:  # Get word
                            word = player.game.round.word
                            send_msg[6] = word
                        elif key == 7:  # Get skips
                            skips = player.game.round.skips
                            send_msg[7] = skips
                        elif key == 8:  # Update board
                            x, y, color = data['8'][:3]
                            player.game.update_board(x, y, color)
                        elif key == 9:  # Get round time
                            t = player.game.round.time
                            send_msg[9] = t
                    if key == 10:
                        raise Exception("Not valid request")

                conn.sendall(json.dumps(send_msg).encode()+".".encode())


            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()}: {e}")
                break

        print(f"[DISCONNECT] {player.name} disconnected")
        # player.game.player_disconnected(player)
        conn.close()

    def handle_queue(self, player):
        """
        Adds player to queue and creates new game if enough players
        :param player: Player
        :return: None
        """
        self.connection_queue.append(player)

        if len(self.connection_queue) >= self.PLAYERS:
            game = Game(self.game_id, self.connection_queue[:])

            for p in self.connection_queue:
                p.set_game(game)

            self.game_id += 1
            self.connection_queue = []

    def authentication(self, conn, addr):
        """
        Authentication here
        :param addr: str
        :param conn: connection object
        :return: None
        """
        try:
            data = conn.recv(1024)
            name = str(data.decode())
            if not name:
                raise Exception("No name received")
            conn.sendall("1".encode())

            player = Player(addr, name)
            self.handle_queue(player)
            thread = threading.Thread(target=self.player_thread, args=(conn, player))
            thread.start()
        except Exception as e:
            print(f"[EXCEPTION] {e}")
            conn.close()

    def connected_thread(self, ):

        server = "188.166.107.89"
        port = 6543

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen(1)
        print("Waiting for a connection, Server started")

        while True:
            conn, addr = s.accept()
            print("[CONNECT] New Connection")

            self.authentication(conn, addr)


if __name__ == "__main__":
    s = Server()
    thread = threading.Thread(target=s.connected_thread)
    thread.start()