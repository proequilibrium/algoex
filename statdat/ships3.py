import socket
import random
import json
from itertools import permutations

alphabet = "ABCDEFGHIJKLMNO"


def genShots():
    nums=range(1,16)
    shots = []
    for i in range(0,15,2):
        if i % 2:
            for j in range(0,15,2):
                shots.append(str(alphabet[i]+str(nums[j])))
        else:
            for j in range(0,15,2):
                shots.append(str(alphabet[i]+str(nums[j])))
    return shots

def squareCombine(yList,xList):
    combined = []
    for y in yList:
        for x in xList:
            combined.append(y + str(x))
    return combined

def onHit(hitShot):
    yAcc = alphabet.index(hitShot[:1])
    xAcc = int(hitShot[1:])
    ymoz = alphabet[yAcc-1:yAcc+2]
    xmoz = range(xAcc-1, xAcc+2)
    comb = squareCombine(ymoz, xmoz)
    comb.remove(hitShot)
    print("targeting: ..{}".format(comb))
    return comb

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("challenges.thecatch.cz", 8000))
    #get greetings
    result = s.recv(4048)
    print(result.decode('utf-8'))
    #get manual
    result = s.recv(4048)
    print(result.decode('utf-8'))

    for round in range(4):
        shots = genShots()
        #get game start
        print("Round {} STARTS -----------{}".format(round, result))
        result = s.recv(4048)
        try:
            game = json.loads(result.decode("utf-8"))
            print(game)
        except json.decoder.JSONDecodeError as e:
            print("ZACATEK TIMEOUT\n", result)
            break

        print("Status {}".format(game['overallResult']))
        lastGame = game
        hitSquare = []
        shoted = []

        while lastGame['overallResult'] == game['overallResult']:
            if not hitSquare:
                shot = random.choice(shots)
                shots.remove(shot)
            else:
                shot = random.choice(hitSquare)
                hitSquare.remove(shot)

            shoted.append(shot)
            s.send(shot.encode())
            result = s.recv(4048)
            try:
                game = json.loads(result.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                print("\n \n NOT JSON \n \n", result)
                break

            if game['yourMoveResult']=='Hit':
               hitSquare = onHit(shot)
               for shotSquare in hitSquare:
                   if shotSquare in shots: shots.remove(shotSquare)
               for shotSquare in hitSquare:
                   if shotS in shoted: hitSquare.remove(shotSquare)
            print("Round {} vysledek {} After shot {} Remaining shots {} my result {} his result {}".format(round, game['overallResult'], shot, len(shots), game['yourMoveResult'], game['myMoveResult']))
