from bs4 import BeautifulSoup
import requests
import re

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
        self.teams = []
        self.players = {99999 : "Dummy Player"}

    def printLeague(self):
        for team in self.teams:
            team.printTeam()

    def addTeam(self, newTeam):
        self.teams.append(newTeam)


if __name__ == "__main__":
    l = League("My League")
    l.printLeague()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
    r  = requests.get("http://games.espn.com/ffl/standings?leagueId=28641&seasonId=2016", headers=headers)
    data = r.text
    soup = BeautifulSoup(data)

    #Create objects for every team in the league
    for tr in soup.find_all('tr', class_='tableBody'):
        teamLink = tr.find('a').get('href') #Link to team
        rawName = tr.find('a').get('title')

        teamOwner = re.match(r".*\((.*?)\).*", rawName).group(1)
        teamName = re.match(r"^(.*?)\(", rawName).group(1)
        teamId = re.match(r".*teamId=([0-9]{1,2}).*", teamLink).group(1)

        newTeam = Team(teamName, teamId, teamOwner)
        l.addTeam(newTeam)

    l.printLeague()
