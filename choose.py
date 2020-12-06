

import copy
# import random


class Choose():
    def __init__(self):

        self.classInfo = StatHolder()
        
   
        self.repeatName = "repeat"
        self.classWeight = {self.validClassHuman[0]: 1.0}

    def getValidClassByNumGhost(self, num):
        ls = []
        for x in self.basicGhost:
            ls.append(x)
        if num > 3:
            ls.append(self.validClassGhostNum[0])
        return ls

    def getValidClassByNumHuman(self, num):
        ls = []
        for x in self.basicHuman:
            ls.append(x)
        ls.append(self.validClassHuman[0])
        return ls

    def getTotalNumGhost(self, num):
        if (num > 4):
            return 2
        return 1

    def getTotalNumHelper(self, num):
        if (num > 3):
            return 0
        return 0

    def getTotalNumOther(self, num):
        return 0

    def makeValidTeams(self, num):
        totalGhost = self.getTotalNumGhost()
        totalHelper = self.getTotalNumHelper()
        totalOther = self.getTotalNumOther()
        totalExtra = 3
        totalHuman = num - (totalGhost+totalHelper+totalOther) + totalExtra
        c0 = ChooseTeam(num, totalGhost, totalHuman, totalHelper,
                        totalOther, self.classInfo)
        self.validTeams = c0

    def returnValidChoose(self):
        ls = []
        return ls


class ChooseTeam():
    def __init__(self, limit, cgh, chu, che, cot, stHolder):
        self.makeGhosts()
        self.totalPlayers = limit
        self.totalGhosts = cgh
        self.totalHumans = chu
        self.totalHelpers - che
        self.totalOther = cot
        self.hold = stHolder

    def makeGhosts():
        ls = []
        for x in range()
        

class StatHolder():
    def __init__(self, cd):
        numRoles = 3
        self.classInfo = []
        for x in range(numRoles):
            self.classInfo.append(ClassStats(x))

    def getClass(self, teamSize, currentTeam, typeWant):
        cs = []
        for x in self.classInfo:
            if (x.getType == typeWant):
                cs.append(x)
        validcs = []
        for x in cs:
            valid = True
            if teamSize < x.getMinTeamSize():
                valid = False
            numAlready = currentTeam.count(x.getClassName())
            if (numAlready >= x.getMaxNum()):
                valid = False
            if valid:
                validcs.append(x)
            

class ClassStats():
    def __init__(self, cd):
        self.classId = cd
        self.setup(self.classId)

    def getType(self):
        return self.type

    def getClassName(self):
        return self.className

    def getMinTeamSize(self):
        return self.minSize

    def getMaxNum(self):
        return self.maxNum

    def getMinNum(self):
        return self.minNum

    def setup(self, d):
        if d == 0:
            self.className = "citizen"
            self.type = "human"
            self.maxNum = -1
            self.minNum = 0
            self.minSize = 0
            self.weight = 0.1
        elif d == 1:
            self.className = "spirit"
            self.type = "ghost"
            self.maxNum = -1
            self.minNum = 0
            self.minSize = 0
            self.weight = 0.1
        elif d == 2:
            self.className = "seer"
            self.type = "human"
            self.maxNum = 1
            self.minNum = 1
            self.minSize = 0
            self.weight = 1.0
