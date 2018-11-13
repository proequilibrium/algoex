import socket
import random
import json
from itertools import permutations

alphabet = "ABCDEFGHIJKLMNO"


def showShoted(shots, hits):
    lajna="showShoted"
    for i in range(1,16):
        print(lajna,)
        lajna=""
        for j in range(15):
            scan = alphabet[j] + str(i)
            if scan in hits:
                lajna+="X"
            elif scan in shots:
                if not scan == shots[-1]:
                    lajna += "v"
                else:
                    lajna += "O"
            else:
                lajna+="-"
    print(lajna, flush=True)


def gentargets():
    nums=range(1,16)
    targets = []
    for i in range(0,15):
        if i % 2:
            for j in range(0,15,2):
                targets.append(str(alphabet[i]+str(nums[j])))
        else:
            for j in range(1,15,2):
                targets.append(str(alphabet[i]+str(nums[j])))
    return targets

def squareCombine(yList,xList):
    combined = []
    for y in yList:
        for x in xList:
            combined.append(y + str(x))
    return combined

def onHit(hitShot, targeded):
    yAcc = alphabet.index(hitShot[:1])
    xAcc = int(hitShot[1:])
    ymoz = alphabet[max(yAcc-1,0):min(yAcc+2,15)]
    xmoz = range(max(xAcc-1,1),min(xAcc+2,16))
    comb = squareCombine(ymoz, xmoz)+targeded
    comb = list(set(comb))
    print("\n targeting: ..{}".format(comb))
    return comb

def verify(squareShot, shoted, targets):
    setSS = set(squareShot)
    setSD = set(shoted)
    setT = set(targets)
    print("Mnoziny ss sd {}, sd t {}, ss t {}".format(setSS & setSD, setSD & setT, setSS & setT))
    if (setSS & setSD or setSD & setT or setSS & setT):
        print('targets ', targets)
        print('targeded', targeted)
        print('\n',shoted,'\n')
        showShoted(shoted, hits)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("challenges.thecatch.cz", 8000))
    #get greetings
    result = s.recv(10)
    print(result.decode('utf-8'))
    #get manual
    result = s.recv(4048)
    print(result.decode('utf-8'))
    shoted=[]
    hits=[]
    for round in range(100):
        hitCount=[0,0]
        targets = gentargets()
        #get game start
        print("Round {} STARTS -----------{}".format(round, result))
        result = s.recv(4048)
        try:
            game = json.loads(result.decode("utf-8"))
            print(game)
        except json.decoder.JSONDecodeError as e:
            print("ZACATEK TIMEOUT\n", result)
            break
        showShoted(shoted, hits)
        print("Status {}".format(game['overallResult']))
        lastGame = game
        targeted = []
        shoted = []
        hits = []

        while lastGame['overallResult'] == game['overallResult']:
            try:
                if not targeted:
                    shot = random.choice(targets)
                    targets.remove(shot)
                else:
                    shot = random.choice(targeted)
                    targeted.remove(shot)
            except Exception as e:
                showShoted(shoted, hits)
                print("vycerpany cile")
            shoted.append(shot)

            s.send(shot.encode())
            result = s.recv(4048)
            try:
                game = json.loads(result.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                showShoted(shoted, hits)
                print("posledni", shoted[-1])
                print("\n\n{}\n\n".format(game['overallResult']))
                print("\n \n KONEC: \n \n", result)
                break

            if game['yourMoveResult']=='Hit':
               hits.append(shot)
               hitCount[0] += 1
               targeted = onHit(shot, targeted)
               targets = list(set(targets) - set(targeted))
               targeted = list(set(targeted) - set(shoted))
            if game['myMoveResult']=='Hit':
               hitCount[1] += 1
               showShoted(shoted, hits)

            #print("Round {} vysledek {} After shot {} Remaining targets {} my result {} his result {}".format(round, game['overallResult'], shot, len(targets), game['yourMoveResult'], game['myMoveResult']))
            print("\n xy {}, my: {} his: {} --{}/{}       {}".format(shot, game['yourMoveResult'], game['myMoveResult'], hitCount[0], hitCount[1], game['overallResult']))
