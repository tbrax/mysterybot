
# import string


class TestSample:
    name = ''


class Character():
    def __init__(self, m, num, dsname):
        self.discordAuth = dsname
        self.name = self.discordAuth.name
        self.characterClass = ""
        self.mystery = m
        self.setClassName()
        self.setWinTeamInitial()
        self.setGhostInitial()
        self.setAppearAsGhost()
        self.num = num
        self.waitText = []
        self.target = self
        self.confused = False

    def setWinTeamInitial(self):
        self.winTeam = "human"

    def getActualTarget(self):
        return self.target

    def setAppearAsGhost(self):
        if self.ghost:
            self.appearGhost = True
        self.appearGhost = False

    def setWinTeam(self, team):
        self.winTeam = team

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

    def useNightAbility(self, target):
        return ""

    def triggerNightAbility(self):
        return self.useNightAbility(self.target)

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
        return "You have no night ability."

    def getInfoString(self):

        if3 = self.getInfoKnown()
        if (if3 != ""):
            if3 += "\n"

        if2 = "Your ability is: {0}. {1}".format(self.nightAbilityName(),
                                                 self.getNightAbility())

        tx = """Your class is {0}\n{1}\n{2}\n{3}{4}""".format(
                        self.className.upper(),
                        self.getGhostInfo(),
                        self.getWinInfo(),
                        if3,
                        if2
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
        self.className = "citizen"


class CharDMV(Character):
    def __init__(self, m, num, dsname):
        Character.__init__(self, m, num, dsname)
        self.dmvgood = "CURRENT"
        self.dmvbad = "NO RECORD"
        self.goodList = ["citizen", "dmv worker"]
        self.badList = []

    def setClassName(self):
        self.className = "dmv worker"

    def nightAbilityName(self):
        return "Check Drivers License"

    def getNightAbility(self):
        ab = 'Choose someone to check their driver license. ' \
            'HUMANS will appear as {0}. ' \
            'Ghosts will appear as {1}.'.format(self.dmvgood, self.dmvbad)
        return ab

    def useNightAbility(self, target):
        ans = "has NO RECORD of a drivers license"
        tName = target.getDisplayName()
        target = self.getActualTarget()
        tClass = target.getClassName()
        if (tClass in self.goodList):
            ans = "has a VALID drivers license"
        elif (tClass in self.badList):
            ans = "has an EXPIRED drivers license"

        wait = "{0} {1}".format(tName, ans)
        self.setWaitText(wait)


class CharDutchman(Character):
    def __init__(self, m, num, dsname):
        Character.__init__(self, m, num, dsname)

    def setClassName(self):
        self.className = "flying dutchman"

    def setWinTeam(self):
        self.winTeam = "ghost"

    def setGhostInitial(self):
        self.ghost = True

    def getInfoKnown(self):
        return self.ghostListText()


class CharSpirit(Character):
    def __init__(self, m, num, dsname):
        Character.__init__(self, m, num, dsname)

    def setClassName(self):
        self.className = "Spirit"

    def setWinTeam(self):
        self.winTeam = "ghost"

    def setGhostInitial(self):
        self.ghost = True

    def getNightAbility(self):
        return "You can kill someone."

    def getInfoKnown(self):
        return self.ghostListText()
