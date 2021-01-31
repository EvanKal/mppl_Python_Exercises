# anoikse vivlio8hkes
import requests
import json
import datetime
import calendar
from multiprocessing import Pool

today = datetime.date.today()
# today = datetime.date.today().replace(day=3)
currentMonth = datetime.date.today().month
monthDescr = calendar.month_name[currentMonth]
gameID = "1100"
firstID = ""
winningNumbersOfFirstDraw = {}
allDrawsResults = []

def initiate():

    allDrawsResults = getAllDrawResultsForCurrentMonth()
    displayStatisticsPerDay(allDrawsResults)

def getAllDrawResultsForCurrentMonth():
    #API returns all draw results for one day at a time
    allDaysToRetrieve = []
    allDaysToRetrieve  = [date for date in calendar.Calendar().itermonthdates(today.year, today.month) if date.month == datetime.date.today().month] 
    allDrawsResults = []
       
    for dayToRetrieveDraws in allDaysToRetrieve:
        url = "https://api.opap.gr/draws/v3.0/{gameId}/draw-date/{fromDate}/{toDate}?limit=180&property=winningNumbers".format(gameId = gameID, fromDate =  dayToRetrieveDraws, toDate = dayToRetrieveDraws)
        print(url)
        results = getDictFromJSONResponse(url)
        results['date']  = dayToRetrieveDraws
        allDrawsResults.append(results)

    return allDrawsResults



def displayStatisticsPerDay(allDrawsResults):
    print("Showing results for current month: {monthDescr}".format(monthDescr=monthDescr))

    if(not allDrawsResults):
        print("No results to show yet")
    else:
        #Itterate over every result per day that contains all 180 draw results of the day
        for resultSet in allDrawsResults:
            print(createDateDescription(resultSet['date']))
            winningNumbers={}
            #WinningNumbers per draw are contained in a 'content' dict under the key 'winningNumbers' 
            for drawResult in resultSet['content']:
                #Itterate over each winningNumber and then add it in winningNumbers dict as a key and increment its occurences counter by one
                for winningNumber in drawResult['winningNumbers']['list']:
                    winningNumbers[winningNumber] = winningNumbers.get(winningNumber, 0) + 1

            print("All winning numbers occurences")
            print(winningNumbers)
            maxOccurences = max(winningNumbers.values())
            numbersWithMaxOccurences = [key for key in winningNumbers.keys() if winningNumbers[key] == maxOccurences]
            print("Max occurence is {max}. {textNumber} with such occurence {textIs}: ".format(max=maxOccurences, textNumber= "Numbers" if len(numbersWithMaxOccurences)>1 else "Number", textIs=  "are" if len(numbersWithMaxOccurences)>1 else "is"))
            print(numbersWithMaxOccurences)


#----------------Utils-------------------------

def createDateDescription(dateToBePrinted):
    day = dateToBePrinted.day
    dayIndex = dateToBePrinted.weekday()
    month = dateToBePrinted.month
    dayDescr = calendar.day_name[dayIndex]
    monthDescr = calendar.month_name[month]
    
    return "Results for {dayDescr} {day} of {monthDescr} {year}:".format(dayDescr=dayDescr, day=day, monthDescr=monthDescr, year=dateToBePrinted.year)

def getDictFromJSONResponse(url):
    r=requests.get(url)
    html=r.text
    data=json.loads(html)
    return data

initiate()