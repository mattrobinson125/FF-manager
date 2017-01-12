from bs4 import BeautifulSoup
from itertools import permutations
import requests
import re
import csv


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

    # Add to the end of the score list
    def addScore(self, score):
        self.scores.append(score)

    # Returns the instance teams score given a week
    def getScoreByWeek(self, weekNum):
        return scores[weekNum + 1]


class League:

    def __init__(self, name="My League"):
        self.name = name
        self.teams = [None] * 12
        self.players = {99999 : "Dummy Player"}
        self.schedule = []
        self.fetchAll()

    #TODO: Explore python __repr__ for print statements
    def printSchedule(self):
        for i, week in enumerate(self.schedule):
            print('Week', i + 1, ':', week)

    #TODO: Explore python __repr__ for print statements
    def printLeague(self):
        for team in self.teams:
            team.printTeam()

    # Add a team to the league
    def addTeam(self, teamId, newTeam):
        self.teams[teamId-1] = newTeam

    # Return the team object given a @tid ()
    def getTeamById(self, tid):
        return self.teams[tid - 1]

    # Returns an outcome list for a given team assignment, such that
    # outcome[i] = number of wins (the TRUE) team i had. The results are NOT
    # ordered according to the @assignment variable, but rather to the
    # leagues TRUE ordering.
    def getOutcome(self, assignment):
        outcome = [0 for i in range(12)]
        for i, week in enumerate(self.schedule):
            for matchup in week:
                team1 = self.getTeamById(assignment[matchup[0] - 1])
                team2 = self.getTeamById(assignment[matchup[1] - 1])
                team1Score, team2Score = team1.scores[i], team2.scores[i]
                if team1Score > team2Score: #t1 win
                    outcome[team1.tid - 1] += 1
                else: #t2 win
                    outcome[team2.tid - 1] += 1
        return outcome

    # Returns an iterator over the outcomes of each season.
    # Outcome format is a list, with the number at index i represinting
    # the number of wins team i finished with
    def simulateAllSeasons(self):
        teams, weeks = len(self.teams), len(self.schedule)
        allPerms = permutations(range(1, 1 + teams))
        winCts = [[0 for i in range(1 + weeks)] for i in range(teams)]
        print("This will take a while...")
        for outcome in map(self.getOutcome, allPerms):
            for i, winCt in enumerate(outcome):
                winCts[i][winCt] += 1
        return winCts

    # Retrieves and returns the winCts, while also writing them to a CSV file.
    def exportWinCts(self):
        data = []
        winCts = self.getAllWinCts()
        for i, teamCts in enumerate(winCts):
            teamOwner = l.getTeamById(i+1).owner
            for winNum, freq in enumerate(teamCts):
                data = data + [[teamOwner, winNum, freq]]
        exportToCSV(data)
        return winCts


    # Calls all web scrapers
    def fetchAll(self):
        self.fetchTeams()
        self.fetchSchedule()

    # Gathers team information, including owner, name, and record
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
    # Imports the schedule of the league, keeping track of the scores that
    # each team earned in any given week.
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
                    score = float(team.find('td', class_='score').get('title'))
                    self.getTeamById(a).addScore(score)
                # add new matchup to this weeks matchup list
                weekSchedule.append(matchup)
            # finally, add week to overall schedule list
            self.schedule.append(weekSchedule)


# Exports a list to a csv file.
def exportToCSV(lst):
    with open('allwincts.csv', 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(lst)


if __name__ == "__main__":
    print("Creating new league and fetching data...")
    l = League("My League")
    l.fetchAll()
    print("Done fetching")
    print(l.__dict__)
