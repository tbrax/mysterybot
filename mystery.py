
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
        self.mainChannel = 0

        self.nameOrder = ["spirit", "flying dutchman",
                          "citizen", "dmv worker",
                          "seer", "cultist"]

        self.choose = Choose(self.nameOrder)

    def getNameOrder(self):
        return self.nameOrder

    def getMainChannel(self):
        return self.mainChannel
    
    def setMainChannel(self, ch):
        self.mainChannel = ch

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

    def getTargetFromText(self, abstr):
        isValidNum = abstr.isnumeric()
        validLen = len(self.characterList)
        if (isValidNum):
            num = int(abstr)
            if (num > 0 and num <= validLen):
                target = self.getTargetByNum(num)
                return target

        return 0

    def useAbility(self, abstr, auth, stage=2):
        ch = self.getCharFromAuth(auth)
        resp = 0
        if (ch != 0):
            tar = self.getTargetFromText(abstr)
            if (tar != 0):
                resp = ch.targetNightAbility(tar)
        return resp

    def useVote(self, abstr, auth, stage=2):
        ch = self.getCharFromAuth(auth)
        resp = 0
        if (ch != 0):
            tar = self.getTargetFromText(abstr)
            if (tar != 0):
                resp = ch.makeVote(tar)
        return resp

    def startVoting(self):
        self.stage = 3

    def isGhostInCharacters(self):
        isGhost = False
        for x in self.characterList:
            if x.getGhost():
                isGhost = True
        return isGhost

    def triggerVoteWin(self, votedList):
        winnerList = []
        for x in self.characterList:
            if (x.triggerWin(votedList)):
                winnerList.append(x)
        return winnerList

    def charsToNameList(self, ls):
        nm = []
        for x in ls:
            nm.append(x.getDisplayName())
        return nm

    def endVoting(self):
        self.stage += 1
        voteList = []
        for x in self.characterList:
            vt = x.getVote()
            if (vt is not 0):
                voteList.append(vt)
        voteName = []
        voteAmt = []
        for x in voteList:
            if x in voteName:
                idx = voteName.index(x)
                voteAmt[idx] += 1
            else:
                voteName.append(x)
                voteAmt.append(1)

        voteHighest = 0
        for x in voteAmt:
            if x > voteHighest:
                voteHighest = x

        voteOut = []
        for x in range(len(voteAmt)):
            if voteAmt[x] == voteHighest:
                voteOut.append(voteName[x])

        nmList = self.charsToNameList(voteName)

        votedStr = "Voting results:\n"
        tstr = ""

        for x in range(len(nmList)):
            tstr += " {0}-{1} ".format(nmList[x], voteAmt[x])
            if (x < len(nmList)-1):
                tstr += ","
        votedStr += "{0}".format(tstr)

        voteValid = True

        totalVote = voteOut

        vstr = ""
        for x in range(len(totalVote)):
            vstr += " {0} ".format(totalVote[x].getDisplayName())
            if (x < len(nmList)-1):
                vstr += ","

        if (voteHighest <= 1):
            votedStr += "\nNot enough votes\n"
            voteValid = False

        if (len(voteOut) >= 3):
            votedStr += "\nToo many people with equal votes\n"
            voteValid = False

        if (not voteValid):
            totalVote = []
        else:
            votedStr += "\nVoted out:\n"
            votedStr += vstr

        roleStr = "\nRoles:\n"
        for x in self.characterList:
            gxt = "HUMAN"
            if x.getGhost():
                gxt = "GHOST"
            roleStr += " {0}({1})({2}) ".format(x.getDisplayName(),
                                                x.getClassName().upper(),
                                                gxt)

        votedStr += roleStr
        winList = self.triggerVoteWin(totalVote)
        winStr = ""
        for x in winList:
            winStr += " {0} ".format(x.getDisplayName())

        votedStr += "\nWinners:\n {0}".format(winStr)
        self.cancelMystery()
        return votedStr

    def endNight(self):
        ls = []
        for x in self.characterList:
            ls.append(x)
        random.shuffle(ls)
        ls.sort(reverse=True)
        for x in ls:
            x.triggerNightAbility()
        self.startVoting()

    def classFromName(self, name, num, auth):
        
        name = name.lower()
        if name == self.nameOrder[0]:
            return CharSpirit(self, num, auth)
        elif name == self.nameOrder[1]:
            return CharDutchman(self, num, auth)
        elif name == self.nameOrder[2]:
            return CharCitizen(self, num, auth)
        elif name == self.nameOrder[3]:
            return CharDMV(self, num, auth)
        elif name == self.nameOrder[4]:
            return CharSeer(self, num, auth)
        elif name == self.nameOrder[5]:
            return CharHelper(self, num, auth)

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
            pNum = num + 3
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
        # availClasses = self.chooseClasses(num)

        avc = self.choose.makeValidTeams(num)
        classText = "Roles in this game:\n"
        authorText = "\nPlayers in this game:\n"

        for x in avc:
            classText += " {0} ".format(x)

        count = 0
        for x in self.listOfDiscordAuthors:
            count += 1
            
            testing = False
            if (count == 1) and (self.testClass):
                testing = True
                gclass = self.testClass

            if not testing:
                idx = random.randint(0, len(avc)-1)
                gclass = avc[idx]
                del avc[idx]

            self.characterList.append(self.classFromName(gclass, count, x))

        for x in self.characterList:
            authorText += " {0} ".format(x.getDisplayName())

        instruInfo = "\nGo to the private message and "\
                     "use your ability by typing the "\
                     "number of the person you want to target"

        return classText + authorText + instruInfo

        # if (len(availClasses) == len(self.listOfDiscordAuthors)):
        #    count = 0
        #    for x in self.listOfDiscordAuthors:
        #        count += 1
        #        idx = random.randint(0, len(availClasses)-1)

        #        if self.testClass:
        #            if self.testClass in availClasses:
        #                idx = availClasses.index(self.testClass)

        #        gclass = availClasses[idx]
        #        del availClasses[idx]
        #        self.characterList.append(self.classFromName(gclass,count,x))


def main():
    m = MysteryClass()

    m.addDiscordTestName("jimmy")
    m.addDiscordTestName("jake")
    m.addDiscordTestName("toby")
    m.addDiscordTestName("jessica")
    m.addDiscordTestName("bob")
    m.addDiscordTestName("mike")

    m.setTestClass("seer")

    print(m.startMystery())

    tx = ""
    for x in m.getCharacterList():
        tx += "{0} {1}, ".format(x.getDisplayName(), x.getClassName())
    print(tx)

    aut = m.listOfDiscordAuthors[0]
    ch0 = m.getCharFromAuth(aut)

    # tx1 = m.useAbility("1",aut)
    print(ch0.getInfoString())

    wantVal = True
    while(wantVal):
        val = input("")
        resp = m.useAbility(val, aut)
        if (resp != 0):
            print(resp)
            wantVal = False

    print(m.endNight())
    print("Night End")
    print(ch0.getWaitText())
    print("Starting voting")

    wantVal = True
    while(wantVal):
        val = input("Enter your vote:")
        resp = m.useVote(val, aut)
        if (resp != 0):
            print(resp)
            wantVal = False
    print(m.endVoting())


if __name__ == "__main__":
    # execute only if run as a script
    main()
