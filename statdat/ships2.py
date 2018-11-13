import socket
import random
import json


def genShots():
    alphabet = "ABCDEFGHIJKLMNO"
    nums=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    shots = []
    for i in range(15):
        for j in range(15):
            shots.append(str(alphabet[i]+str(nums[j])))
    return shots

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("challenges.thecatch.cz", 8000))
    #get greetings
    result = s.recv(4048)
    print(result.decode('utf-8'))
    #get manual
    result = s.recv(4048)
    print(result.decode('utf-8'))

    for round in range(100):
        shots = genShots()
        #get game start
        print("Round {} STARTS -----------{}".format(round, result))
        result = s.recv(4048)
        try:
            game = json.loads(result.decode("utf-8"))

        except json.decoder.JSONDecodeError as e:
            print("ZACATEK TIMEOUT\n", result)
            break

        print("Status {}".format(game['overallResult']))
        lastGame = game

        while lastGame['overallResult'] == game['overallResult']:
            shot = random.choice(shots)
            shots.remove(shot)
            s.send(shot.encode())
            result = s.recv(4048)
            try:
                game = json.loads(result.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                print("Telo---------------------------- \n", result)
            print("Round {} vysledek {} After shot {} Remaining shots {} my res:{} his res:{}".format(round, game['overallResult'], shot, len(shots), game['yourMoveResult'], game['myMoveResult']))
