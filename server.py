import socket
from _thread import *
import pickle
from game import Game

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Server Started, Waiting for a connection...")

games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if data == "get":
                    reply = game
                elif data == "reset":
                    game.reset()
                    reply = game
                elif data.startswith("add:"):
                    _, choice = data.split(":")
                    game.add_choice(p, choice)
                    reply = game
                elif data.startswith("commit:"):
                    _, choice = data.split(":")
                    game.commit_choice(p, choice)
                    reply = game
                else:
                    reply = game

                conn.sendall(pickle.dumps(reply))
            else:
                break

        except:
            break

    print("Lost connection to Player", p)
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
