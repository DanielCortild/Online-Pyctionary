import socket
import threading
from player import Player
from game import Game
import json

try:
    import logging
    from systemd.journal import JournalHandler
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    logger.addHandler(JournalHandler())

    def log(msg):
        logger.info(msg)
except:
    def log(msg):
        print(msg)


class Server:
    PLAYERS = 2

    def __init__(self):
        self.connection_queue = []
        self.game_id = 0
        self.addr = ("", 1287)

    def player_communication(self, conn, player):
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

                if key == -2:
                    send_msg = [True if player.game else False, len(self.connection_queue), self.PLAYERS]
                if key == -1:  # Get list of players
                    if player.game:
                        send_msg = {
                            player.get_name(): player.get_score() for player in player.game.players
                        }
                    else:
                        send_msg = {}
                if player.game:
                    if key == 0:  # Guess
                        if not player.has_guessed:
                            guess = player.game.player_guess(player, data['0'][0])
                            if guess:
                                player.update_score(player.game.round.time)
                                player.has_guessed = True
                            send_msg = guess
                    #elif key == 1:  # Skip
                    #    send_msg = player.game.skip()
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
                    #elif key == 7:  # Get skips
                    #    send_msg = player.game.round.skips
                    elif key == 8:  # Update board
                        player.game.update_board(*data['8'][:3])
                    elif key == 9:  # Get round time
                        send_msg = player.game.round.time
                    elif key == 10:  # Get whether you are drawing or not
                        send_msg = player.game.players[player.game.player_draw_ind-1] == player
                    elif key == 11:  # Clear the board
                        player.game.board.clear()
                    elif key == 13:  # Get name of drawer
                        send_msg = player.game.players[player.game.player_draw_ind - 1].get_name()
                if key == 12:
                    send_msg = True if player.game else False

                conn.sendall(json.dumps(send_msg).encode()+".".encode())

            except Exception as e:
                log(f"[!ERROR!] {player.get_name()}: {e}")
                break

        log(f"[DISCONN] {player.name} ({player.ip[0]})")
        try:
            if player in self.connection_queue:
                self.connection_queue.remove(player)
            # if player.game:
                # player.game.player_disconnected(player)
        except:
            pass
        conn.close()

    def handle_queue(self, player):
        """
        Adds given player to queue and starts new game if sufficient number of players
        :param player: Player
        :return: None
        """
        self.connection_queue.append(player)

        if len(self.connection_queue) >= self.PLAYERS:
            game = Game(self.connection_queue[:])
            for p in game.players:
                p.set_game(game)
            self.game_id += 1
            self.connection_queue = []

    def authentication(self, conn, addr):
        """
        Authenticates the user and launches a player thread
        :param conn: Connection Object
        :param addr: (str, int)
        :return: None
        """
        try:
            name = conn.recv(1024).decode()
            if not name:
                raise Exception(f"No name received ({addr[0]})")
            conn.sendall("[CONNECT]".encode())

            player = Player(addr, name)
            self.handle_queue(player)
            log(f"[CONNECT] {name} ({addr[0]})")

            threading.Thread(target=self.player_communication, args=(conn, player)).start()
        except Exception as e:
            log(f"[!ERROR!] {e}")
            conn.close()

    def start(self):
        """
        Starts the Network
        :return: None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(self.addr)
        except socket.error as e:
            log(f"[SOCKET!] {e}")

        sock.listen(1)
        log("[STARTED] Waiting for a connection")

        while True:
            conn, addr = sock.accept()
            self.authentication(conn, addr)


if __name__ == "__main__":
    # s = Server()
    # threading.Thread(target=s.connected_thread).start()
    Server().start()