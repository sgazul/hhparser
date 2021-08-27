# Created by Stanislav Gazul (stanislav@gazul.ru) based on other scripts across the Internet
# Output csv file could be view in MS Excel by "Import" feauture (please use Transform data option to use first row as the header)
import requests
import time
import random
import os
from bs4 import BeautifulSoup as bs
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
OutputFilePath = 'output.csv'
VacancionsCounter = 0 # Vacansions counter
SitePageNumber = 0 # HH pages counter for specified vacancy
print("Welcome to the SMG headhunter parser.")
print("Please enter city code for Headhunter site.")
print("For Moscow press '1', for St. Petersburg press '2'")
CityCode = input() # Input Region code
print("Please input site pages quantity to parse. The parser will work until first error.")
SitePageNumberLimit = input() # Input pages quantity
print("Input vacancy title to collect")
FindingVacancyTitle = input() # Input finding vacancy
OutputFile = open(OutputFilePath, 'a', encoding='utf-8-sig') # Opening the file to write with specified encoding
TableHeader = 'Название_вакансии,Город,Заработная_плата,Ссылка_на_вакансию,Название_организации,Условия_и_требования \n'
OutputFile.write(TableHeader) # Writing the header for our output table in file. It's specified above
def hh_parse(URL, headers): # Main function to the HH pages parsing
    global VacancionsCounter
    Session = requests.session()
    FirstRequest = Session.get(URL, headers=headers)
    if FirstRequest.status_code == 200: # If everything ok - starting to find standard vacancies fields. If script isn't working, first thing to chech if attrs names is changed
        global SitePageNumberLimit
        global CityCode
        global FindingVacancyTitle
        soup = bs(FirstRequest.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'}) + soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'}) + soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus'})
        for div in divs:
            # Trying to get data from page objects
            try:
                Title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text # Trying to get vacancy title
            except:
                Title = 'Not specified'
            try:
                Compensation = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text # Trying to get salary value
            except:
                Compensation = 'Not specified'
            CurrentVacancyUrl = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href'] # Trying to get the ling
            try:
                Company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text # Trying to get company name
            except:
                Company = 'Not specified'
            try:
                Address = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text # Trying to get address (city and subway station names)
            except:
                Address = 'Not specified'
            Session = requests.session()
            SecondRequest = Session.get(CurrentVacancyUrl, headers=headers) # Get the current vacancy page
            if SecondRequest.status_code == 200: # If ok, lets parse it. If script isn't working, first thing to chech if attrs names is changed
                soup = bs(SecondRequest.content, 'html.parser')
                try:
                    VacancyDescription = soup.find('div', attrs={'data-qa': 'vacancy-description'}).text # Trying to get FULL vacancy description inside the current vacancy page
                except:
                    VacancyDescription = 'Not specified'
            CurrentVacancy = '"' +  Title + '","' + Address + '","' + Compensation + '","' + CurrentVacancyUrl + '","' + Company + '","' + VacancyDescription + '"\n' # Getting the current vacancy string
            OutputFile.write(CurrentVacancy) # And writting it to the file
            #print(CurrentVacancy) # It is debug option. Uncomment it to see every written vacancy in console
            VacancionsCounter = VacancionsCounter + 1 # Count the new vacancy
            os.system("cls") # Clean console output for updating counters in a single row and show meeting lines
            print("Welcome to the SMG headhunter parser.")
            print('Working... Please wait for a while until counter will stopped.')
            print('The city code is: ' + str(CityCode))
            print(str(SitePageNumberLimit) + ' HH pages going to be parsed if they are exist. The parser will work until first error.')
            print('We are finding all vacancies contains: ' + str(FindingVacancyTitle))
            print('Current vacancy number: ' + str(VacancionsCounter) + '. Current site page number: ' + str(SitePageNumber)) # And print it's number and current page number
    else: # If status code isn't 200 - print "Error!".
        print('Error!')
        print('Last collected vacancy number is: ' + str(VacancionsCounter-1) + '. Last site page number: ' + str(SitePageNumber-1)) # Print the last stats
        exit()
while SitePageNumber <= int(SitePageNumberLimit): #while not specified page count exceeds
    URL = 'https://hh.ru/search/vacancy?area=' + str(CityCode) + '&text=' + str(FindingVacancyTitle) + '&page=' + str(SitePageNumber) # Forming next URL to visit
    time.sleep(random.randint(5,15)) # Waiting for a random count of seconds from 5 to 15
    hh_parse(URL, headers)
    SitePageNumber = SitePageNumber + 1
print('Last collected vacancy number is: ' + str(VacancionsCounter-1) + '. Last site page number: ' + str(SitePageNumber-1)) # Print the last stats
OutputFile.close()
