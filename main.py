import re
import urllib
from urllib import request
from bs4 import *
import datetime
import calendar

now = datetime.datetime.now()
movieList= []
months = dict(January=1, February=2, March=3, April=4, May=5, June=6,
              July=7, August=8, September=9, October=10, November=11, December=12)

def initProgram():#to create the main text file
    f = open('mainText.txt', 'w')
    f.close()

def createInputTexts():
    year = now.year
    month = now.month
    while month < 13:
        monthStr = calendar.month_name[month].lower()
        if month < 10:
            url= 'https://www.imdb.com/movies-coming-soon/' + str(year) + '-0' + str(month) + '/'
        else:
            url = 'https://www.imdb.com/movies-coming-soon/' + str(year) + '-' + str(month) + '/'
        #print(url)
        u = urllib.request.urlopen(url)
        x = u.read().decode('UTF-8')
        soup = BeautifulSoup(x, 'html.parser')
        f = open(monthStr + '_coming.txt', 'w')
        f.write(soup.text)
        f.close()

        if month == 12:
            month = 1
            year += 1
            continue
        if month == now.month - 1:
            break
        month += 1

def addToMainText(inputStr):
    f = open(inputStr, 'r')#inputStr example: april_coming.txt
    f2 = open('mainText.txt', 'a')
    f2.write(f.read())
    f.close()
    f2.close()

def findFromName(name): #returns the movie object with the given name
    for i in movieList:
        if i.name.lower() == name.lower():
            return i


class Movie:
    fullDate = ''
    fullDateYear = ''
    fullDateMonth = ''#like april, may...
    fullDateDay = ''
    def __init__(self, name, year, length ='', genre ='', metascore ='', description ='', director ='', stars =''):
        self.name = name
        self.year = year
        self.length = length
        self.genre = genre
        self.metascore = metascore
        self.description = description
        self.director = director
        self.stars = stars

        movieList.append(self)


    def printMovie(self):
        print(self.name)
        print("Production Year:", self.year)
        print("Release date: " + str(self.fullDateYear) + "-" + str(months[self.fullDateMonth]) + "-" + str(self.fullDateDay))
        #print("Movie length:", self.length)
        print("Genre:", self.genre)
        #print("Metascore:", self.metascore)
        print("Synopsis:", self.description)
        print("Director:", self.director)
        print("Stars:", self.stars)


def initAndReset():

    movieList.clear()
    file = open('mainText.txt', 'r')
    fullText = file.read()
    file.close()

    movieNames = []
    movieYears = []
    textfile = open('mainText.txt', 'r')
    filetext = textfile.readlines()
    textfile.close()


    for lines in filetext:
        if re.match("\s[A-Z].*\(\d{4}\)", lines):
            Films = re.match("\s[A-Z].*\(\d{4}\)", lines)
            Films = Films.group()
            Films = Films.strip()
            movieNames.append(Films[:-7])
            movieYears.append(Films[-5:-1])
        elif re.match("\s\d.*\(\d{4}\)", lines):
            Films = re.match("\s\d.*\(\d{4}\)", lines)
            Films = Films.group()
            Films = Films.strip()
            movieNames.append(Films[:-7])
            movieYears.append(Films[-5:-1])

    #print(movieNames)
    #print(len(movieNames))


    textInOneLine = re.sub("\n", " ", fullText)


    movieNo = 0
    while movieNo < len(movieNames):


        movieNameToTextEnd = re.search(''+movieNames[movieNo]+' \(\d{4}\).*', textInOneLine)
        movieEndToTextEnd = re.search('if\s*\(typeof.*', movieNameToTextEnd.group())

        size = len(movieNameToTextEnd.group())-len(movieEndToTextEnd.group())

        j = 0
        movieInfo = ""
        while j < size:
            movieInfo += movieNameToTextEnd.group()[j]
            j += 1

        #print(movieInfo)


        name = movieNames[movieNo]
        year = movieYears[movieNo]
        length = ''
        genre =''
        metascore =''
        description =''
        director =''
        stars =''


        movieInfo = movieInfo.replace(name, '')
        movieInfo = movieInfo.replace('(' + year + ')', '')


        if re.search("\d+\smin", movieInfo) is not None: #for length
            length = re.search("\d+\smin", movieInfo).group()
            movieInfo = movieInfo.replace(length, '') #Iterating

        if re.search('[0-9]+\s+Metascore', movieInfo) is not None: #for Metascore
            metaS = re.search('[0-9]+\s+Metascore', movieInfo).group()
            movieInfo = movieInfo.replace(metaS, '') #Iterating
            metaS = re.split("\s", metaS)
            metascore = metaS[0]

        #tidying up the info a bit.
        movieInfo = movieInfo.strip()
        movieInfo = re.search("[A-Z].*", movieInfo).group() #it's like strip, to get rid of unnecessary symbols like '-' from the head of the string

        #this part is for genre. All movies must have at least one genre for this to work, and they do have at least one, so here it is:
        tempListForGenre = re.split('\s\s\s\s', movieInfo)

        genre = tempListForGenre[0]
        genre = re.sub(' \|', ',', genre)

        movieInfo = movieInfo.replace(tempListForGenre[0], '') #Iterating
        movieInfo = movieInfo.strip()
        del tempListForGenre
        #genre part is over.

        #This part is for description. Same situation with genre
        tempListForDesc = re.split('\s\s\s\s', movieInfo)
        description = tempListForDesc[0]

        movieInfo = movieInfo.replace(tempListForDesc[0], '') #Iterating
        movieInfo = movieInfo.strip()
        del tempListForDesc
        #description part is over

        #director and stars part
        directorToEnd = ''
        starsToEnd = ''
        onlyDirector = ''
        if re.search("Director[s]*: .*", movieInfo) is not None:
            directorToEnd = re.search("Director[s]*: .*", movieInfo).group()
        if re.search("Stars: .*", movieInfo) is not None:
            starsToEnd = re.search("Stars: .*", movieInfo).group()
        onlyDirector = directorToEnd.replace(starsToEnd, '')

        if onlyDirector is not '' or None:
            director = onlyDirector.replace('Director: ', '')
            director = director.replace('Directors: ', '')
            director = director.replace('  | ', ',')
            director = director.strip()
        if starsToEnd is not '' or None:
            stars = starsToEnd.replace('Stars: ', '')
            stars = stars.replace('  ', ' ')
            stars.strip()
        #director and stars part is over

        movie = Movie(name, year, length, genre, metascore, description, director, stars)

        movieNo += 1

        #movie.printMovie()
        #print()


def addTheFullDates():#adds the full dates to all the movies inside movieList
    tempFile = open('mainText.txt', 'r')
    tempText = tempFile.readlines()
    tempFile.close()
    date = ""

    for x in tempText:
        if re.match("[A-Z][a-z]+\s[1-3][0-9]", x):#catch the date
            date = re.match("[A-Z][a-z]+\s[1-3][0-9]", x).group()
            #print(date)

        elif re.match("[A-Z][a-z]+\s[0-9]", x):#catch the date
            date = re.match("[A-Z][a-z]+\s[0-9]", x).group()
            #print(date)

        if re.match("\s[A-Z].*\(\d{4}\)", x):#catch the movie object and add the date
            #objWithMovieName.fullDate = date
            findFromName(re.match("\s[A-Z].*\(\d{4}\)", x).group()[:-7].strip()).fullDate = date
            findFromName(re.match("\s[A-Z].*\(\d{4}\)", x).group()[:-7].strip()).fullDateMonth = re.split(' ', date)[0]
            findFromName(re.match("\s[A-Z].*\(\d{4}\)", x).group()[:-7].strip()).fullDateDay = re.split(' ', date)[1]

            if int(months[re.split(' ', date)[0]]) >= now.month:
                findFromName(re.match("\s[A-Z].*\(\d{4}\)", x).group()[:-7].strip()).fullDateYear = now.year
            else:
                findFromName(re.match("\s[A-Z].*\(\d{4}\)", x).group()[:-7].strip()).fullDateYear = now.year + 1

        elif re.match("\s\d.*\(\d{4}\)", x):#catch the movie object and add the date
            #objWithMovieName.fullDate = date
            findFromName(re.match("\s\d.*\(\d{4}\)", x).group()[:-7].strip()).fullDate = date
            findFromName(re.match("\s\d.*\(\d{4}\)", x).group()[:-7].strip()).fullDateMonth = re.split(' ', date)[0]
            findFromName(re.match("\s\d.*\(\d{4}\)", x).group()[:-7].strip()).fullDateDay = re.split(' ', date)[1]

            if int(months[re.split(' ', date)[0]]) >= now.month:
                findFromName(re.match("\s\d.*\(\d{4}\)", x).group()[:-7].strip()).fullDateYear = now.year
            else:
                findFromName(re.match("\s\d.*\(\d{4}\)", x).group()[:-7].strip()).fullDateYear = now.year + 1


    #for x in movieList:
        #print(x.name, x.fullDate)


print("Hello! Please wait...")
initProgram()
createInputTexts()#slows down the program. It is okay to run this function only once a month, when the imdb
# database is updated.

haveBeenAddedToMainText = []


print("Please enter a command:")
userInput = input()

while userInput.lower() != 'exit':
    userInput = userInput.split(" ")


    if userInput[0] == 'INPUT':
        if userInput[1] not in haveBeenAddedToMainText:
            print("Loading " + userInput[1] + " ...")
            addToMainText(userInput[1])
            initAndReset()
            addTheFullDates()
            haveBeenAddedToMainText.append(userInput[1])
        else:
            print(userInput[1]+ " has already been loaded.")
            print("Please enter another command:")
            userInput = input()
            continue


    if userInput[0] == 'LIST':
        if len(userInput) == 1:#if the whole input is list
            print("Listing ...")
            for x in movieList:
                print(x.name)
            #print()

        elif userInput[1][0] == 'f':#from, from-to
            if len(userInput) == 2:#list with from
                print("Listing " + userInput[1] + " ...")
                fromDate = userInput[1].split('-')
                fromDate[0] = fromDate[0][-4:]#fromDate is yyyy, mm, dd
                year = fromDate[0]
                month = fromDate[1]
                day = fromDate[2]

                for x in movieList:
                    if int(year) < int(x.fullDateYear):
                        print(x.name)
                    elif int(year) == int(x.fullDateYear):
                        if int(month) < int(months[x.fullDateMonth]):
                            print(x.name)
                        elif int(month) == int(months[x.fullDateMonth]):
                            if int(day) <= int(x.fullDateDay):
                                print(x.name)

            elif len(userInput) == 3:#list with from and to
                print("Listing " + userInput[1] + " " + userInput[2] + " ...")
                fromDate = userInput[1].split('-')
                fromDate[0] = fromDate[0][-4:]  # fromDate is yyyy, mm, dd
                yearFrom = fromDate[0]
                monthFrom = fromDate[1]
                dayFrom = fromDate[2]

                toDate = userInput[2].split('-')
                toDate[0] = toDate[0][-4:]  # toDate is yyyy, mm, dd
                yearTo = toDate[0]
                monthTo = toDate[1]
                dayTo = toDate[2]

                allowedToPrint = None

                for x in movieList:
                    if int(yearFrom) < int(x.fullDateYear):
                        allowedToPrint = True
                    elif int(yearFrom) == int(x.fullDateYear):
                        if int(monthFrom) < int(months[x.fullDateMonth]):
                            allowedToPrint = True
                        elif int(monthFrom) == int(months[x.fullDateMonth]):
                            if int(dayFrom) <= int(x.fullDateDay):
                                allowedToPrint = True
                            else:
                                allowedToPrint = None
                        else:
                            allowedToPrint = None
                    else:
                        allowedToPrint = None

                    if allowedToPrint:
                        if int(yearTo) > int(x.fullDateYear):
                            allowedToPrint = True
                        elif int(yearTo) == int(x.fullDateYear):
                            if int(monthTo) > int(months[x.fullDateMonth]):
                                allowedToPrint = True
                            elif int(monthTo) == int(months[x.fullDateMonth]):
                                if int(dayTo) >= int(x.fullDateDay):
                                    allowedToPrint = True
                                else:
                                    allowedToPrint = None
                            else:
                                allowedToPrint = None
                        else:
                            allowedToPrint = None

                    if allowedToPrint:
                        print(x.name)

        elif userInput[1][0] == 'g':  #genre
            genreList = re.split(':', userInput[1])[1]
            genreList = re.split(',', genreList)
            print(genreList)

            for x in movieList:
                genresOfMovie = re.split(', ', x.genre)
                if set(genreList).issubset(genresOfMovie):
                    print(x.name)

    if userInput[0] == 'INFO':
        print("Info ...")
        tempName = ' '.join(userInput)
        tempName = re.sub('INFO', '', tempName)
        tempName = tempName.strip()
        x = findFromName(tempName)
        x.printMovie()





    print("Please enter a command:")
    userInput = input()
    #end of while





