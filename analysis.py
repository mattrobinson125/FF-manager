from bs4 import BeautifulSoup
import requests
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}

class Team:

    def __init__(self, name, tid, owner):
        self.name = name
        self.tid = tid
        self.owner = owner
        self.scores = []

    def printTeam(self):
        print("Name:", self.name, ", Team ID:",
            self.tid, ", Owner:", self.owner)

    def addScore(self, score):
        scores.append(score)


class League:

    def __init__(self, name):
        self.name = name
        self.teams = [None] * 12
        self.players = {99999 : "Dummy Player"}
        self.schedule = []

    def printLeague(self):
        for team in self.teams:
            team.printTeam()

    def addTeam(self, teamId, newTeam):
        self.teams[teamId-1] = newTeam

    def getTeamById(self, id):
        return self.schedule[id]

    def fetchTeams(self):
        r  = requests.get("http://games.espn.com/ffl/standings?leagueId=28641&seasonId=2016", headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        #Create objects for every team in the league
        for tr in soup.find_all('tr', class_='tableBody'):
            teamLink = tr.find('a').get('href') #Link to team
            rawName = tr.find('a').get('title')

            teamOwner = re.match(r".*\((.*?)\).*", rawName).group(1)
            teamName = re.match(r"^(.*?)\(", rawName).group(1)
            teamId = int(re.match(r".*teamId=([0-9]{1,2}).*", teamLink).group(1))

            newTeam = Team(teamName, teamId, teamOwner)
            self.addTeam(teamId, newTeam)

    def fetchSchedule(self):
        for i in range(1,14): #iterate over every week in the regular season schedule
            url = "http://games.espn.com/ffl/scoreboard?leagueId=28641&matchupPeriodId={}".format(i)
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            weekSchedule = []
            for game in soup.find_all('table', class_='ptsBased matchup'): #every matchup in the week
                matchup = () #int tuple
                for team in game.find_all('tr')[:-1]:
                    a = int(re.match(r".*_([0-9]{1,2})_.*", team.get('id')).group(1)) #get id of team in matchup
                    matchup = matchup + (a,)
                weekSchedule.append(matchup)

            self.schedule.append(weekSchedule)


if __name__ == "__main__":
    l = League("My League")
    l.fetchSchedule()
    print(l.schedule)

    l.fetchTeams()
    l.printLeague()
