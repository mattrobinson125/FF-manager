
class Team:
    def __init__(self, name, tid, owner):
        self.name = name
        self.tid = tid
        self.owner = owner

    def printTeam(self):
        print("Name:", self.name, ", Team ID:",
            self.tid, ", Owner:", self.owner)

class League:
    def __init__(self, name):
        self.name = name
        #self.teams = []
        self.teams = [Team("Team 1", 7, "Matt Robinson"),
                     Team("Team 2", 0, "Derek Zahoruiko")]
        self.players = {99999 : "Dummy Player"}

    def printLeague(self):
        for team in self.teams:
            team.printTeam()


if __name__ == "__main__":
    l = League("My League")
    l.printLeague()
