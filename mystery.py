
import string
import copy
import random
from maincharacter.character import *
from choose import Choose

class MysteryClass():
    def __init__(self):
        self.timeSecondsNight = 60
        self.timeSecondsDay = 60
        self.basicHuman = "citizen"
        self.basicGhost = "spirit"
        self.validClassGhost = ["spirit", "flying dutchman"]
        self.validClassHuman = ["citizen", "dmv worker"]
        self.validClassGhostHelper = ["cultist"]
        self.cancelMystery()
        self.testClass = False
        self.choose = Choose()

    def cancelMystery(self):
        self.stage = 0
        self.listOfPartNames = []
        self.listOfDiscordAuthors = []
        self.characterList = []
        self.globalMessages = []
        

    def addGlobalMessage(self, msg):
        self.globalMessages.append(msg)

    def getSecondsNight(self):
        return self.timeSecondsNight

    def setSecondsNight(self, secc):
        self.timeSecondsNight = int(secc)

    def getSecondsDay(self):
        return self.timeSecondsDay

    def setSecondsDay(self, sec):
        self.timeSecondsDay = int(sec)

    def setupMystery(self):
        self.stage = 1

    def acceptingCharacters(self):
        return self.stage == 1

    def getStage(self):
        return self.stage

    def getCharFromAuth(self, auth):
        for x in self.characterList:
            if (x.getDiscordAuth() == auth):
                return x
        return 0

    def getGhostList(self):
        ls = []
        for x in self.characterList:
            if (x.getGhost()):
                ls.append(x)
        return ls

    def useAbility(self, abstr, auth, stage=2):
        ch = self.getCharFromAuth(auth)
        isValidNum = abstr.isnumeric()
        validLen = len(self.characterList)
        resp = 0
        if (isValidNum and ch != 0):
            num = int(abstr)
            if (num >= 0 and num < validLen):
                target = self.getTargetByNum(num)
                resp = ch.targetNightAbility(target)
        return resp

    def endNight(self):
        ls = []
        for x in self.characterList:
            ls.append(x)
        ls.sort(reverse=True)
        for x in ls:
            x.triggerNightAbility()

    def classFromName(self, name, num, auth):
        if name == self.validClassHuman[0]:
            return CharCitizen(self, num, auth)
        elif name == self.validClassHuman[1]:
            return CharDMV(self, num, auth)
        elif name == self.validClassGhost[0]:
            return CharSpirit(self, num, auth)
        elif name == self.validClassGhost[1]:
            return CharDutchman(self, num, auth)

        return CharCitizen(self, num, auth)

    def getCharacterList(self):
        return self.characterList

    def addDiscordAuthor(self, aut):
        if (aut in self.listOfDiscordAuthors):
            return 0
        self.listOfDiscordAuthors.append(aut)
        return 1

    def addDiscordTestName(self, n):
        auth = TestSample()
        auth.name = n
        self.listOfDiscordAuthors.append(auth)

    def getDiscordAuthorList(self):
        return self.listOfDiscordAuthors

    def getParticipantString(self):
        stList = ""
        for x in range(len(self.listOfDiscordAuthors)):
            stList += "{0} {1}".format(x, self.listOfPartNames[x].name)
        return stList

    def getNumGhostActual(self, num):
        if (num > 4):
            return 2
        return 1

    def getNumGhostHelpActual(self, num):
        if (num > 5):
            return 1
        return 0

    def potentialGhostList(self, num):
        potentialList = []
        listGrab = copy.deepcopy(self.validClassGhost)
        pNum = 3
        if (num > 4):
            pNum = 4
        elif (num > 5):
            pNum = 5
        for x in range(pNum):

            classPicked = self.basicGhost
            if (len(listGrab) > 0):
                idx = random.randint(0, len(listGrab)-1)
                classPicked = listGrab[idx]
                del listGrab[idx]

            potentialList.append(classPicked)       
        return potentialList

    def potentialHumanList(self, num):
        potentialList = []
        listGrab = copy.deepcopy(self.validClassHuman)
        pNum = num+1
        if (num > 4):
            pNum = num+2
        elif (num > 6):
            pNum = num+3 
        for x in range(pNum):
            classPicked = self.basicHuman
            if (len(listGrab) > 0):
                idx = random.randint(0, len(listGrab)-1)
                classPicked = listGrab[idx]
                del listGrab[idx]
            potentialList.append(classPicked)       
        return potentialList

    def validClass(self, mysteryclass, numPlayersRemain):
        return True

    def chooseClasses(self, num):

        # num = len(characterLst)
        availableClassGhost = self.potentialGhostList(num)

        availableClassHuman = self.potentialHumanList(num)

        availableClassHelper = []

        numGhost = self.getNumGhostActual(num)
        numHelper = self.getNumGhostHelpActual(num)
        numHuman = num - (numGhost + numHelper)
        chosenClasses = []

        for x in range(numGhost):
            if (len(availableClassGhost) > 0):
                idx = random.randint(0, len(availableClassGhost)-1)
                if self.testClass:
                    if self.testClass in availableClassGhost:
                        idx = availableClassGhost.index(self.testClass)
                iclass = availableClassGhost[idx]
                del availableClassGhost[idx]
                chosenClasses.append(iclass)

        for x in range(numHelper):
            if (len(availableClassHelper) > 0):
                idx = random.randint(0, len(availableClassHelper)-1)

                if self.testClass:
                    if self.testClass in availableClassHelper:
                        idx = availableClassHelper.index(self.testClass)
                iclass = availableClassHelper[idx]
                del availableClassHelper[idx]
                chosenClasses.append(iclass)

        for x in range(numHuman):
            if (len(availableClassHuman) > 0):
                idx = random.randint(0, len(availableClassHuman)-1)
                if self.testClass:
                    if self.testClass in availableClassHuman:
                        idx = availableClassHuman.index(self.testClass)
                iclass = availableClassHuman[idx]
                del availableClassHuman[idx]
                chosenClasses.append(iclass)

        # ##################################
        return chosenClasses

    def getTargetByNum(self, target):
        target -= 1
        if (target >= 0 and target < len(self.characterList)):
            return self.characterList[target]
        return 0

    def setTestClass(self, test):
        self.testClass = test

    def startMystery(self):
        self.stage = 2
        num = len(self.listOfDiscordAuthors)
        availClasses = self.chooseClasses(num)
        print(availClasses)
        if (len(availClasses) == len(self.listOfDiscordAuthors)):
            count = 0
            for x in self.listOfDiscordAuthors:
                count += 1
                idx = random.randint(0, len(availClasses)-1)

                if self.testClass:
                    if self.testClass in availClasses:
                        idx = availClasses.index(self.testClass)

                gclass = availClasses[idx]
                del availClasses[idx]
                self.characterList.append(self.classFromName(gclass,count,x))

def main():
    m = MysteryClass()

    m.addDiscordTestName("jimmy")
    m.addDiscordTestName("jake")
    m.addDiscordTestName("toby")
    m.addDiscordTestName("jessica")
    m.addDiscordTestName("bob")

    m.setTestClass("dmv worker")

    m.startMystery()

    tx = ""
    for x in m.getCharacterList():
        tx += "{0} {1}, ".format(x.getDisplayName(),x.getClassName())
    print(tx)

    aut = m.listOfDiscordAuthors[0]    
    ch0 = m.getCharFromAuth(aut)

    #tx1 = m.useAbility("1",aut)
    print(ch0.getInfoString())

    wantVal = True
    while(wantVal):
        val = input("Enter your value: ")
        resp = m.useAbility(val, aut)
        if (resp != 0):
            print(resp)
            wantVal = False

    m.endNight()
    print("Night End")
    print(ch0.getWaitText())

if __name__ == "__main__":
    # execute only if run as a script
    main()