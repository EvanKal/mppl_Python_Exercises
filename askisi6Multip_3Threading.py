# anoikse vivlio8hkes
import requests
import json
import datetime
import calendar
from multiprocessing import Lock
import threading


currentMonth = datetime.date.today().month
monthDescr = calendar.month_name[currentMonth]
gameID = "1100"
allDrawsResults = []
threadIndent=0

def initiate():
    
    getAllDrawResultsForCurrentMonth()
    displayStatisticsPerDay(allDrawsResults)

def getAllDrawResultsForCurrentMonth():
    today = datetime.date.today()
    # today = datetime.date.fromisoformat("2021-02-01")
    allDaysToRetrieve = []
    allDaysToRetrieve  = [date for date in calendar.Calendar().itermonthdates(today.year, today.month) if date.month == today.month and date <= today] 
    
    multiProcessCallsToAPI(allDaysToRetrieve)

def multiProcessCallsToAPI(allDaysToRetrieve):
    allResults=[]
    if __name__ == '__main__':        
        lock = Lock()

        # Create an event to handle the way the results from the call get gathered
        e = threading.Event()

        #Gather all processes in a list so that I can handle their execution
        allThreads = [threading.Thread(target=getResultsPerDay, args=(lock, e, day, index)) for index, day in enumerate(allDaysToRetrieve)]
          
        #Fire all API calls concurrently in multple Threads with no concern about index
        for thread in allThreads:
            thread.start()
        
        #Join all threads after they have been fired concurrrently so that they can terminate gracefully
        for thread in allThreads:
            thread.join()

def getResultsPerDay(l, e, dayToRetrieveDraws, index):
    global allDrawsResults
    global threadIndent
    
    #API returns all draw results for one day at a time so limit is set to 180 to get all draw results in one call, but seperate calls for each day need to be made
    url = "https://api.opap.gr/draws/v3.0/{gameId}/draw-date/{fromDate}/{toDate}?limit=180&property=winningNumbers".format(gameId = gameID, fromDate =  dayToRetrieveDraws, toDate = dayToRetrieveDraws)
    print(url)
    results = getDictFromJSONResponse(url)
    results['date']  = dayToRetrieveDraws
    
    #Wait until previous threads have completed writing to global variable 'allDrawsResults'
    while index != threadIndent:
        e.wait()

    #If thread index is the one that should write to 'allDrawsResults' then go on
    l.acquire()
    try:
        print("Released thread with index ", index)
        allDrawsResults.append(results)
        threadIndent = index + 1
    finally:
        l.release()
        #Set event to true for next thread to release and write the results it holds to 'allDrawsResults'
        e.set()

def displayStatisticsPerDay(allDrawsResults):

    if(not allDrawsResults[0]['content']):
        print("No results to show yet")
    else:
        print("Showing results for current month: {monthDescr}".format(monthDescr=monthDescr))
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