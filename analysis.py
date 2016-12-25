from bs4 import BeautifulSoup
import requests
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) ' +
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}

class Team:

    def __init__(self, name, tid, owner):
        self.name = name
        self.tid = tid
        self.owner = owner
        self.scores = []

    #TODO: Explore python __repr__ for print statements
    def printTeam(self):
        print("Name:", self.name, ", Team ID:",
            self.tid, ", Owner:", self.owner)

    def addScore(self, score):
        self.scores.append(score)


class League:

    def __init__(self, name):
        self.name = name
        self.teams = [None] * 12
        self.players = {99999 : "Dummy Player"}
        self.schedule = []

    #TODO: Explore python __repr__ for print statements
    def printSchedule(self):
        for i, week in enumerate(self.schedule):
            print('Week', i + 1, ':', week)

    #TODO: Explore python __repr__ for print statements
    def printLeague(self):
        for team in self.teams:
            team.printTeam()

    def addTeam(self, teamId, newTeam):
        self.teams[teamId-1] = newTeam

    def getTeamById(self, tid):
        return self.teams[tid - 1]

    def fetchAll(self):
        self.fetchTeams()
        self.fetchSchedule()

    def fetchTeams(self):
        url = "http://games.espn.com/ffl/standings?leagueId=28641&seasonId=2016"
        r  = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        #Create objects for every team in the league
        for teamData in soup.find_all('tr', class_='tableBody'):
            teamLink = teamData.find('a').get('href') #Link to team for id parsing
            rawName = teamData.find('a').get('title') #Get team name

            # Extract team info from input of format "Team Name (Owner Name)"
            # and team id from URL of format "/ffl/clubh...&teamId=id&..."
            teamOwner = re.match(r".*\((.*?)\).*", rawName).group(1)
            teamName = re.match(r"^(.*?)\(", rawName).group(1)
            teamId = int(re.match(r".*teamId=([0-9]{1,2}).*", teamLink).group(1))

            newTeam = Team(teamName, teamId, teamOwner)
            self.addTeam(teamId, newTeam)

    # NOTE: This function is dependent on the teams being imported already.
    # Potentially refactor to remove this dependency.
    def fetchSchedule(self):
        #iterate over every week in the regular season schedule
        baseUrl = "http://games.espn.com/ffl/scoreboard?leagueId=28641&matchupPeriodId="
        for i in range(1,14):
            r = requests.get(baseUrl + "{}".format(i), headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            weekSchedule = []
            # for every matchup in the week
            for game in soup.find_all('table', class_='ptsBased matchup'):
                matchup = ()
                for team in game.find_all('tr')[:-1]:
                    #get id of each team in matchup from url, add to matchup tuple
                    a = int(re.match(r".*_([0-9]{1,2})_.*", team.get('id')).group(1))
                    matchup = matchup + (a,)
                    # add score to teams list of scores
                    score = team.find('td', class_='score').get('title')
                    self.getTeamById(a).addScore(score)
                # add new matchup to this weeks matchup list
                weekSchedule.append(matchup)
            # finally, add week to overall schedule list
            self.schedule.append(weekSchedule)


if __name__ == "__main__":
    l = League("My League")
    l.fetchAll()
    #l.printSchedule()

    print(l.__dict__)
    #l.printLeague()
