import socket
import random
import json

abcd_sel = 'ABCDEFGHIJKLMNO'


class Shot:
    shot_desk = [[False] * 15]* 15
    shotYX = ""

    def __init__(self, newShot):
        self.shotYX = newShot

    def __str__(self):
        return self.shotYX

    def __repr__(self):
        return self.shotYX

    def getShotY(self):
        return abcd_sel.index(self.shotYX[0])

    def getShotX(self):
        return int(self.shotYX[1])

    def getBin(self):
        return str.encode(self.shotYX)

def getRandShot():

    print("rand shot")
    # return string with 2 characters "char and digit"
    return Shot(random.choice(abcd_sel) + str(random.randrange(1,16)))

def getBoxShot(lastShot):
    xSelect = random.choice([-1, 1])
    ySelect = random.choice([-1, 1])
    yStr = abcd_sel[(lastShot.getShotY()+ySelect)%16+1]
    xStr = str((lastShot.getShotX()+xSelect)%16+1)
    return Shot(yStr + xStr)

def makeShot(lastShotResult, lastShot):
    shot = getRandShot() if not lastShotResult=='Hit' else getBoxShot(lastShot)
    while Shot.shot_desk[shot.getShotY()][shot.getShotX()]:
        print("rehit",shot,end=' ')
        shot = getRandShot() if not lastShotResult=='Hit' else getBoxShot(lastShot)
    Shot.shot_desk[shot.getShotY()][shot.getShotX()] = True
    return shot


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("challenges.thecatch.cz", 8000))

#get greetings
result = s.recv(4048)
print(result.decode('utf-8'))
#get manual
result = s.recv(4048)
print(result.decode('utf-8'))

for round in range(1):
    #get game start
    print("Round {} STARTS -----------".format(round))
    result = s.recv(4048)
    game = json.loads(result.decode('utf-8'))
    print("Status {}".format(game['overallResult']))
    lastRoundResult = game
    shot = getRandShot()
    shots = []

    while lastRoundResult['overallResult'] == game['overallResult']:
        shot = makeShot(game['yourMoveResult'], shot)
        shots.append(shot)
        print(shot)
        s.send(shot.getBin())
        result = s.recv(4048)
        game = json.loads(result.decode("utf-8"))
        print("Round {} After shot {} result:{}".format(round, shot, game['yourMoveResult']))
s.close()
