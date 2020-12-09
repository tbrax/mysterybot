

# import copy
import random


class Choose():
    def __init__(self, nameOrder):

        self.classInfo = StatHolder(nameOrder)

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
        if (num > 5):
            return 1
        return 0

    def getTotalNumOther(self, num):
        return 0

    def getTotalNumExtra(self, num):
        if (num > 8):
            return 4
        elif (num > 5):
            return 3
        elif (num > 3):
            return 2
        return 1

    def makeValidTeams(self, num):
        totalGhost = self.getTotalNumGhost(num)
        totalHelper = self.getTotalNumHelper(num)
        totalOther = self.getTotalNumOther(num)
        totalExtra = self.getTotalNumExtra(num)
        totalHuman = num - (totalGhost+totalHelper+totalOther) + totalExtra
        c0 = ChooseTeam(num, totalGhost, totalHuman, totalHelper,
                        totalOther, self.classInfo)

        ls = c0.makeTeam()

        return ls
        # self.validTeams = c0

    def returnValidChoose(self):
        ls = []
        return ls


class ChooseTeam():
    def __init__(self, limit, cgh, chu, che, cot, stHolder):
        self.totalPlayers = limit
        self.totalGhosts = cgh
        self.totalHumans = chu
        self.totalHelpers = che
        self.totalOther = cot
        self.hold = stHolder

    def makeTeam(self):
        ls = []
        l0 = self.makeGhosts()
        ls += l0
        l1 = self.makeHumans()
        ls += l1
        l2 = self.makeHelpers()
        ls += l2
        return ls

    def makeGhosts(self):
        wnt = "ghost"
        ls = []
        for x in range(self.totalGhosts):
            gh = self.hold.getClass(self.totalPlayers, ls, wnt)
            if (gh is not 0):
                ls.append(gh.getClassName())
            else:
                print("Could not get enough roles")
        return ls

    def makeHumans(self):
        wnt = "human"
        ls = []
        for x in range(self.totalHumans):
            gh = self.hold.getClass(self.totalPlayers, ls, wnt)
            if (gh is not 0):
                ls.append(gh.getClassName())
            else:
                print("Could not get enough roles")
        return ls

    def makeHelpers(self):
        wnt = "helper"
        ls = []
        for x in range(self.totalHelpers):
            gh = self.hold.getClass(self.totalPlayers, ls, wnt)
            if (gh is not 0):
                ls.append(gh.getClassName())
            else:
                print("Could not get enough roles")
        return ls


class StatHolder():
    def __init__(self, nameOrder):
        numRoles = len(nameOrder)
        self.classInfo = []
        for x in range(numRoles):
            self.classInfo.append(ClassStats(x, nameOrder))

    def getClass(self, teamSize, currentTeam, typeWant):
        cs = []
        for x in self.classInfo:
            if (x.getType() == typeWant):
                cs.append(x)
        validcs = []
        for x in cs:
            valid = True
            if teamSize < x.getMinTeamSize():
                valid = False
            numAlready = currentTeam.count(x.getClassName())
            gm = x.getMaxNum()
            if ((gm is not -1) and (numAlready >= gm)):
                valid = False
            if valid:
                validcs.append(x)

        if (len(validcs) == 0):
            return 0

        weightss = []
        for x in validcs:
            weightss.append(x.getWeight())

        cho = random.choices(validcs, weights=weightss)
        return cho[0]
        # retClassIdx = random.randint(0, len(validcs)-1)
        # return validcs[retClassIdx]


class ClassStats():
    def __init__(self, cd, nameOrder):
        self.classId = cd
        self.setup(self.classId, nameOrder[self.classId])

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

    def getWeight(self):
        return self.weight

    def setup(self, d, nam):
        self.className = nam
        if d == 0:
            # spirit
            self.type = "ghost"
            self.maxNum = -1
            self.minNum = 0
            self.minSize = 0
            self.weight = 0.1
        elif d == 1:
            # flying dutchman
            self.type = "ghost"
            self.maxNum = 1
            self.minNum = 0
            self.minSize = 4
            self.weight = 0.2
        elif d == 2:
            # citizen
            self.type = "human"
            self.maxNum = -1
            self.minNum = 0
            self.minSize = 0
            self.weight = 0.1
        elif d == 3:
            # dmv worker
            self.type = "human"
            self.maxNum = 1
            self.minNum = 0
            self.minSize = 2
            self.weight = 0.15
        elif d == 4:
            # seer
            self.type = "human"
            self.maxNum = 1
            self.minNum = 1
            self.minSize = 0
            self.weight = 1000.0
        elif d == 5:
            # cultist
            self.type = "helper"
            self.maxNum = 1
            self.minNum = 1
            self.minSize = 6
            self.weight = 0.1
