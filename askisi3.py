# anoikse vivlio8hkes
import requests
import json
import datetime
import calendar

# today = datetime.date.today()
today = datetime.date.today().replace(day=3)
currentMonth = datetime.date.today().month
monthDescr = calendar.month_name[currentMonth]
gameID = "1100"
firstID = ""
winningNumbersOfFirstDraw = {}
allDrawsResults = []


def initiate():
    global firstID
    global winningNumbersOfFirstDraw
    global allDrawsResults

    firstID = getFirstDrawOfToday()
    winningNumbersOfFirstDraw = getWinningNumbers(firstID)
    allDrawsResults = getAllDrawResultsForCurrentMonth()
    print("First game ID of {date} is: {gameid} ".format(date=today, gameid=firstID))
    print("Winning numbers are: {winningNumbers}, bonus: {bonus}".format(winningNumbers=winningNumbersOfFirstDraw['list'], bonus=winningNumbersOfFirstDraw['bonus']))
    computeStatistics()

def getFirstDrawOfToday():
    url = "https://api.opap.gr/draws/v3.0/{gameId}/draw-date/{fromDate}/{toDate}/draw-id".format(gameId = gameID, fromDate =  today, toDate = today)
    data = getDictFromJSONResponse(url)
    return data[0]

def getWinningNumbers(drawId):
    url = "https://api.opap.gr/draws/v3.0/{gameId}/{drawId}".format(gameId = gameID, drawId = drawId)
    data = getDictFromJSONResponse(url)
    print(data.keys())
    return data['winningNumbers']

def getAllDrawResultsForCurrentMonth():
    #API returns all draw results for one day at a time
    allDrawsResults = []
    dayToRetrieveDraws = datetime.date.today().replace(day=1)
    url = "https://api.opap.gr/draws/v3.0/{gameId}/draw-date/{fromDate}/{toDate}?limit=180&property=winningNumbers".format(gameId = gameID, fromDate =  dayToRetrieveDraws, toDate = dayToRetrieveDraws)


    while today > dayToRetrieveDraws:
        print(url)
        allDrawsResults.append(getDictFromJSONResponse(url))
        nextDay = dayToRetrieveDraws.day + 1
        print(nextDay)
        dayToRetrieveDraws = dayToRetrieveDraws.replace(day=nextDay)
        url = "https://api.opap.gr/draws/v3.0/{gameId}/draw-date/{fromDate}/{toDate}?limit=180&property=winningNumbers".format(gameId = gameID, fromDate =  dayToRetrieveDraws, toDate = dayToRetrieveDraws)

    return allDrawsResults
    
def computeStatistics():
    print("Showing statistics for {month}".format(month = monthDescr))
    #TODO
    return
#----------------Utils-------------------------

def getDictFromJSONResponse(url):
    r=requests.get(url)
    html=r.text
    data=json.loads(html)
    return data

initiate()

