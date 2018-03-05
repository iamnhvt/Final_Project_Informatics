from flask import Flask, request, render_template, Markup
from collections import defaultdict
import numpy as np
import csv
import matplotlib
import matplotlib.cm as cm

'''This function cleans all the read data:
- Delete all empty cell
- Remove all empty space in string read
'''
def cleanData(fileData):

    # Delete empty row
    for i in range(len(fileData)):
        if (not fileData[i]):
            del(fileData[i])

    # Remove empty space
    for line in fileData:
        for  i in range(len(line)):
            line[i] = line[i].strip()

''' This function is an important one of this assignment
 - It reads all the data from csv file, then transform and clean it
 - Next, it will assign read data into reasonable data structure
 - The use of data structure is stipulated in more details in README.txt
'''
def getData():
    femalesHIVFile = open('data/femalesHIV.csv')
    femalesHIVData = list(csv.reader(femalesHIVFile))[4:]

    malesHIVFile = open('data/malesHIV.csv');
    malesHIVData = list(csv.reader(malesHIVFile))[4:]

    totalGDPFile = open("data/totalGDP.csv")
    totalGDPData = list(csv.reader(totalGDPFile))[4:]

    populationFile = open("data/population.csv")
    populationData = list(csv.reader(populationFile))[4:]

    regionFile = open("data/region.csv")
    regionData = list(csv.reader(regionFile))

    agePercentageFile = open("data/youngAgePercentage.csv")
    agePercentageData = list(csv.reader(agePercentageFile))

 

    # Delete empty rows
    cleanData(femalesHIVData)
    cleanData(malesHIVData)
    cleanData(totalGDPData)
    cleanData(regionData)
    cleanData(populationData)
    cleanData(agePercentageData)

    yearDict = {}
    signDictionary = {}
    allCountries = {}

    # Add females HIV data to each country for each year
    for row in femalesHIVData[1:]:
        # Assign the name of the country to its sign
        signDictionary[row[1]] = row[0]

        # The year data starts from columns 4, so iterates all of the columns
        for i in range(4, len(femalesHIVData[0])):
            # If the data is empty, do not process it
            if (not row[i]):
                row[i] = 0
            currentYear = femalesHIVData[0][i]

            # If the current year has been not processed yet, create a dictionary as a value for it
            if currentYear not in yearDict:
                yearDict[currentYear] = {}

            # If the country has been not processed yet, create a dictionary as a value for it
            yearDict[currentYear][row[0]] = defaultdict(int)
            yearDict[currentYear][row[0]]["femalesHIV"] = float(row[i])

    # Add males HIV data to each country for each year
    for row in malesHIVData[1:]:
        for i in range(4, len(malesHIVData[0])):
            if (not row[i]):
                row[i] = 0

            currentYear = malesHIVData[0][i]
            
            yearDict[currentYear][row[0]]["malesHIV"] = float(row[i])
            

    # Add toal GDP data to each country for each year
    for row in totalGDPData[1:]:
        for i in range(4, len(totalGDPData[0])):
            if (not row[i]):
                row[i] = 0
            currentYear = totalGDPData[0][i]
            
            if row[0] in yearDict[currentYear]:
                yearDict[currentYear][row[0]]["totalGDP"] = float(row[i])/(10**9)         

    # Add population data to each country for each year
    for row in populationData[1:]:
        for i in range(4, len(populationData[0])):
            if (not row[i]):
                row[i] = 0
            currentYear = populationData[0][i]
            
            if row[0] in yearDict[currentYear]:
                yearDict[currentYear][row[0]]["population"] = float(row[i])
                yearDict[currentYear][row[0]]["GDPPP"] = (yearDict[currentYear][row[0]]["totalGDP"] * (10**9)) / float(row[i]) if (row[i]) else 0
    
    for row in agePercentageData[1:]:
        # The year data starts from column 3
        for i in range(3, len(row)):
            # If the row contains non-float value, break the loop
            try:
                currentValue = float(row[i])
            except ValueError:
                break
            # Since the country name is this csv file has some different country name. Therefore,
            # we use the country code in this csv file to link to the country name in other file
            currentCountry = signDictionary[row[1]]
            # Get the current year, since the year in csv is sorted in ascending order
            currentYear = str(1990 + i - 3)

            if currentCountry in yearDict[currentYear]:
                # The population of current Country of current year
                tmpPopulation = yearDict[currentYear][currentCountry]['population']
                # If this is a percentage population of female
                if 'female' in row[2]:
                    yearDict[currentYear][currentCountry]['femalesPopulation'] += currentValue * tmpPopulation /100
                else:
                    yearDict[currentYear][currentCountry]['malesPopulation'] += currentValue * tmpPopulation /100


    # Find all unique countries
    for year in range(1990, 2016):
        for country in yearDict[str(year)]:
            allCountries[country] = {}

    
    # Add region, sign, and income type for each country
    for row in regionData[1:]:
        if row[0] in signDictionary:
            country = signDictionary[row[0]]
            if country in allCountries:  
                allCountries[country]['sign'] = row[0] 
                allCountries[country]['region'] = row[1]
                allCountries[country]['income'] = row[2]
                

    #Delete all the surplus areas, which no not have specific region
    surplusArea = []
    for country in allCountries:
        if ('region' not in allCountries[country] or (not allCountries[country]['region'])):
            surplusArea.append(country)

    for area in surplusArea:
        del allCountries[area]

    for year in range(1990, 2016):
        for country in yearDict[str(year)]:
            if country in allCountries:
                if 'statistics' not in allCountries[country]:
                    allCountries[country]['statistics'] = {}
                allCountries[country]['statistics'][str(year)] = yearDict[str(year)][country]

    return yearDict, allCountries
