
# import string
import random

class TestSample:
    def __init__(self):
        self.name = ""
    def getDisplayName(self):
        return self.name

class Character():
    def __init__(self, m, num, dsname):
        self.discordAuth = dsname
        self.name = self.discordAuth.name
        self.characterClass = ""
        self.mystery = m
        self.setClassName()
        self.setGhostInitial()
        self.setWinTeamInitial()
        self.num = num
        self.waitText = []
        self.target = self
        self.confused = False
        self.forcedTarget = 0
        self.voted = 0
        self.didWin = 0
        self.isFool = False
        self.setAppearAsGhost()
        
        self.bonusKnownText = []

    def getName(self):
        return self.name

    def getFool(self):
        return self.isFool

    def addBonusKnownText(self, txt):
        self.bonusKnownText.append(txt)

    def setFool(self, f):
        self.isFool = f

    def setForcedTarget(self, tar):
        self.forcedTarget = tar

    def setWinTeamInitial(self):
        if (self.ghost):
            self.winTeam = "ghost"
        else:
            self.winTeam = "human"

    def setConfused(self):
        self.confused = True

    def getActualTarget(self):
        if (self.confused):
            ls = self.mystery.getCharacterList()
            idx = random.randint(0, len(ls)-1)
            while (ls[idx] == self.target):
                idx = random.randint(0, len(ls)-1)
            return ls[idx]

        if (self.forcedTarget is not 0):
            return self.forcedTarget

        return self.target

    def setAppearAsGhost(self):
        if self.ghost:
            self.appearGhost = True
        else:
            self.appearGhost = False

    def getAppearAsGhost(self):
        return self.appearGhost

    def setWinTeam(self, team):
        self.winTeam = team

    def makeVote(self, target):
        self.voted = target
        ans = "You voted for {0}".format(target.getDisplayName())
        return ans

    def getVoteMe(self, votedList):
        return [self]

    def getVote(self):
        return self.voted

    def triggerWin(self, votedOut):
        self.didWin = self.checkIfWin(votedOut)
        return self.didWin

    def checkIfWin(self, votedOut):
        isGhostInVoted = False
        isEvenGhost = self.mystery.isGhostInCharacters()
        for x in votedOut:
            if x.getGhost():
                isGhostInVoted = True

        for x in votedOut:
            if x.getFool():
                return False

        if (len(votedOut) == 0):
            if isEvenGhost:
                if self.winTeam == "human":
                    return False
                if self.winTeam == "ghost":
                    return True
            else:
                if self.winTeam == "human":
                    return True
                if self.winTeam == "ghost":
                    return False

        if isEvenGhost:
            if (isGhostInVoted):
                if self.winTeam == "human":
                    return True
                if self.winTeam == "ghost":
                    return False
            else:
                if self.winTeam == "ghost":
                    return True

        return False

    def getSpeed(self):
        return 0

    def __lt__(self, other):
        return self.getSpeed() < self.getSpeed()

    def getWaitText(self):
        tx = ""
        for x in self.waitText:
            tx += "{0}\n".format(x)

        return tx

    def setWaitText(self, text):
        self.waitText.append(text)

    def getCharacterList(self):
        return self.mystery.getCharacterList()

    def getWinTeam(self):
        return self.winTeam

    def setGhostInitial(self):
        self.ghost = False

    def getDisplayName(self):
        return "{1}({0})".format(self.num, self.name)

    def getGhost(self):
        return self.ghost

    def setGhost(self, g):
        self.ghost = g
        if (self.ghost):
            self.setWinTeam("ghost")

    def useNightAbility(self, target, source):
        return

    def triggerNightAbility(self):
        self.useNightAbility(self.target, self)

    def nightAbilityName(self):
        return "No night ability"

    def targetNightAbility(self, target):
        self.target = target
        return "You will target {0} with {1}".format(target.getDisplayName(),
                                                     self.nightAbilityName())

    def getTargetByNum(self, target):
        return self.mystery.getTargetByNum(target)

    def setClassName(self):
        self.className = "invalid class"

    def getClassName(self):
        return self.className

    def getGhostInfo(self):
        if (self.ghost):
            return "You are a GHOST"
        return "You are a HUMAN"

    def getWinInfo(self):
        wn = self.getWinTeam()
        if (wn == "ghost"):
            return "You want the GHOSTS to win. Trick everyone into voting a "\
                    "human out."
        elif (wn == "human"):
            return "You want the HUMANS to win. Find a ghost and "\
                    "vote them out."

    def getNightAbility(self):
        return ""

    def nightAbilityPrompt(self):
        return "Enter the number of your target"

    def getInfoString(self):

        if3 = self.getInfoKnown()
        if (if3 != ""):
            if3 += "\n"

        if2 = "Your ability is: {0}. {1}".format(self.nightAbilityName(),
                                                 self.getNightAbility())
        if (self.getNightAbility() == ""):
            if2 = "You have no night ability"


        tx = """Your class is {0}\n{1}\n{2}\n{3}{4}\n{5}""".format(
                        self.className.upper(),
                        self.getGhostInfo(),
                        self.getWinInfo(),
                        if3,
                        if2,
                        self.nightAbilityPrompt()
                        )
        return tx

    def getGhostList(self):
        return self.mystery.getGhostList()

    def getDiscordAuth(self):
        return self.discordAuth

    def getInfoKnown(self):
        return ""

    def ghostListText(self):
        ls = self.getGhostList()
        num = len(ls)
        tx = "There are no GHOSTS"
        if (num > 0):
            atx = ""
            for x in ls:
                atx += x.getDisplayName() + " "

            tx = "The GHOSTS are: {0}".format(atx)
        return tx

    def getResponseAtStage(self, stage):
        return ""


class CharCitizen(Character):
    def __init__(self, m, num, dsname):
        Character.__init__(self, m, num, dsname)

    def setClassName(self):
        self.className = "Citizen"

    def nightAbilityPrompt(self):
        return ""

    def targetNightAbility(self, target):
        self.target = target
        return ""


class CharDMV(Character):
    def __init__(self, m, num, dsname):
        Character.__init__(self, m, num, dsname)
        self.dmvgood = "CURRENT"
        self.dmvbad = "EXPIRED"
        self.dmvother = "NO RECORD"
        ns = m.getNameOrder()
        # citizen, dmv worker
        self.goodList = [ns[2], ns[3]]
        # seer
        self.badList = [ns[4]]

    def getSpeed(self):
        return 30

    def setClassName(self):
        self.className = "Dmv-Worker"

    def nightAbilityName(self):
        return "Check Drivers License"

    def getNightAbility(self):
        ab = 'Choose someone to check their driver license. ' \
            'CITIZEN and DMV WORKER will appear as {0}. ' \
            'SEER will appear as {1}. '\
            'Other roles will appear as {2}.'.format(self.dmvgood,
                                                     self.dmvbad,
                                                     self.dmvother)
        return ab

    def useNightAbility(self, target, source):
        ans = "has NO RECORD of a drivers license"
        tName = target.getDisplayName()
        target = source.getActualTarget()
        tClass = target.getClassName()
        if (tClass in self.goodList):
            ans = "has a VALID drivers license"
        elif (tClass in self.badList):
            ans = "has an EXPIRED drivers license"
        wait = "{0} {1}".format(tName, ans)
        source.setWaitText(wait)


class CharSeer(Character):
    def __init__(self, m, num, dsname):
        Character.__init__(self, m, num, dsname)

    def setClassName(self):
        self.className = "Seer"

    def setWinTeam(self):
        self.winTeam = "human"

    def setGhostInitial(self):
        self.ghost = False

    def nightAbilityName(self):
        return "Check for Ghostlyness"

    def getNightAbility(self):
        return "Choose someone to check if they are a ghost or not."

    def useNightAbility(self, target, source):
        tName = target.getDisplayName()
        target = source.getActualTarget()
        ans = "HUMAN"
        if (target.getAppearAsGhost()):
            ans = "GHOST"
        wait = "{0} appears as a {1}".format(tName, ans)
        source.setWaitText(wait)


class CharDutchman(Character):
    def __init__(self, m, num, dsname):
        Character.__init__(self, m, num, dsname)

    def setClassName(self):
        self.className = "Flying Dutchman"

    def setWinTeam(self):
        self.winTeam = "ghost"

    def setGhostInitial(self):
        self.ghost = True

    def getInfoKnown(self):
        return self.ghostListText()

    def nightAbilityName(self):
        return "Davy Jone's Locker"

    def getNightAbility(self):
        return "You can send someone to the depths. Turns a HUMAN into a GHOST."

    def useNightAbility(self, target, source):
        tName = target.getDisplayName()
        target = source.getActualTarget()
        tg = target.getGhost()

        if not target.getGhost():
            davyTxt = "Sent to the locker! You have become a GHOST."\
                      "To win, vote a HUMAN out!"
            target.setWaitText(davyTxt)
            target.setGhost(True)
            target.setAppearAsGhost()
            wait = "{0} has become a ghost.".format(tName)
            source.setWaitText(wait)
        else:
            wait = "{0} was already a ghost. Nothing has happened".format(tName)
            source.setWaitText(wait)


class CharSpirit(Character):
    def __init__(self, m, num, dsname):
        Character.__init__(self, m, num, dsname)

    def setClassName(self):
        self.className = "Spirit"

    def setWinTeam(self):
        self.winTeam = "ghost"

    def getSpeed(self):
        return 0

    def setGhostInitial(self):
        self.ghost = True

    def getInfoKnown(self):
        return self.ghostListText()


class CharHelper(Character):
    def __init__(self, m, num, dsname):
        Character.__init__(self, m, num, dsname)

    def setClassName(self):
        self.className = "Cultist"

    def setWinTeam(self):
        self.winTeam = "ghost"

    def getSpeed(self):
        return 0

    def setGhostInitial(self):
        self.ghost = False
        
    def setWinTeamInitial(self):
        self.winTeam = "ghost"

    def getInfoKnown(self):
        return self.ghostListText()

    def getWinInfo(self):
        return "You want the GHOSTS to win. Trick everyone into voting a "\
            "human out. If there are no ghosts, someone other than you "\
            "must be voted out"

    def checkIfWin(self, votedOut):
        isGhostInVoted = False
        isEvenGhost = self.mystery.isGhostInCharacters()
        for x in votedOut:
            if x.getGhost():
                isGhostInVoted = True

        for x in votedOut:
            if x.getFool():
                return False

        if (len(votedOut) == 0):
            if isEvenGhost:
                if self.winTeam == "ghost":
                    return True
            else:
                return False

        if isEvenGhost:
            if (isGhostInVoted):
                if self.winTeam == "human":
                    return True
                if self.winTeam == "ghost":
                    return False
            else:
                if self.winTeam == "ghost":
                    if self not in votedOut:
                        return True

        return False
