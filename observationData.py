from collections import defaultdict
import csv
import dataProcessing


def hiv_vs_year(yearDict):
    '''returns a dictionary of years vs Hiv rates world
    wide for those years'''
    year_HIV = {}
    for year in range(1990, 2016):
        total_population = float(yearDict[str(year)]["World"]["population"])
        male_rate = float(yearDict[str(year)]["World"]["malesHIV"])
        female_rate = float(yearDict[str(year)]["World"]["femalesHIV"])
       
        # For each year, we store the statistics for males, females, and both sex
        if male_rate > 0 and female_rate > 0:
            year_HIV[year] = {'males': float(male_rate), 'females': float(female_rate), 'bothSex': (male_rate + female_rate)/2};
    return year_HIV


def hiv_region(allCountries, yearDict):
    """Takes allCoutries, yearDict, regions and in the period of 1990 to 2015.
    it returns a list of regions and the percentage of the HIV population they represent"""

    hiv_by_region = defaultdict(list)
    #add up the total population with HIV in each region in allCountries
    for country in allCountries:
        for year in range(1990, 2016):
            # Calculate the numver of males and females affected by HIV
            numFemalesHIV = yearDict[str(year)][country]["femalesHIV"] * yearDict[str(year)][country]["femalesPopulation"] / 100
            numMalesHIV =  yearDict[str(year)][country]["malesHIV"] * yearDict[str(year)][country]["malesPopulation"] /100
            # If the statistics are positive, append it to the region data
            if numMalesHIV > 0 and numFemalesHIV > 0:
                hiv_by_region[allCountries[country]["region"]].append(numMalesHIV + numFemalesHIV)

    # Calculate the average amount of people with HIV in these region for 25 years
    for region, value in hiv_by_region.items():
        hiv_by_region[region] = [sum(value)/26]
        # If there is no data for region, delete it
    return hiv_by_region

''' This functions returns the type of population based on the number of population
'''
def type_of_population(numPopulation):
    if numPopulation < 1000000:
        return 'Lower Population'
    elif numPopulation < 10000000:
        return 'Low Population'
    elif numPopulation < 30000000:
        return 'Middle Population'
    elif numPopulation < 80000000:
        return 'Upper Middle Population'
    else:
        return 'High Population'

def hiv_vs_population(allCountries, yearDict):
    """Takes allCoutries, yearDict, regions in the period of 1990 to 2015.
    it returns a dictionary of regions and the percentage of the HIV population they represent"""

    hiv_by_population = defaultdict(list)
    #add up the total population with HIV in each region in allCountries
    for country in allCountries:
        for year in range(1990, 2016):
            # Each year stores a statistics for males and females
            typePopulation = type_of_population(yearDict[str(year)][country]["population"])
            if yearDict[str(year)][country]["malesHIV"] > 0 and yearDict[str(year)][country]["femalesHIV"] > 0:
                hiv_by_population[typePopulation].append([yearDict[str(year)][country]["malesHIV"],
                                                             yearDict[str(year)][country]["femalesHIV"]])

    # Calculate the average rate of people with HIV in these region for 25 years
    for population, value in hiv_by_population.items():
        hiv_by_population[population][0][0] = sum([pair[0] for pair in value]) / len(value)
        hiv_by_population[population][0][1] = sum([pair[1] for pair in value]) / len(value)

    return hiv_by_population


def income_v_hiv(allCountries, yearDict):
    """Takes allCountries, yearDict as arguments in the period of 1990 to 2015.
    it then returns a dictionary representing an income group and the percentage of people with HIV they represent"""

    #create a dictionary of income groups vs HIV
    hiv_n_income = defaultdict(list)
    #for every country add their HIV population to the value of each income group
    for country in allCountries:
        for year in range(1990, 2016):
            # Calculate the number by take the average of males and females then multiply by the population
            numFemalesHIV = yearDict[str(year)][country]["femalesHIV"] * yearDict[str(year)][country]["femalesPopulation"] / 100
            numMalesHIV =  yearDict[str(year)][country]["malesHIV"] * yearDict[str(year)][country]["malesPopulation"] / 100
            if numMalesHIV > 0 and numFemalesHIV > 0:
                hiv_n_income[allCountries[country]["income"]].append(numFemalesHIV + numMalesHIV)
                

    # Calclate the average amount of people with HIV in these income class each year
    for income, value in hiv_n_income.items():
        hiv_n_income[income] = [sum(value)/26]
    
    return hiv_n_income

def male_vs_females(allCountries, yearDict):
    '''Calculate the total number of males and females affected by HIV from 1990 to 2015 across the world'''
    # Number of males and females affected by HIV
    totalMalesHiv = 0
    totalFemalesHiv = 0
    for country in allCountries:
        for year in range(1990, 2016):
            # Calculate the number by take the average of males and females then multiply by the population
            numFemalesHIV = yearDict[str(year)][country]["femalesHIV"] * yearDict[str(year)][country]["femalesPopulation"] / 100
            numMalesHIV =  yearDict[str(year)][country]["malesHIV"] * yearDict[str(year)][country]["malesPopulation"] /100
            if numMalesHIV > 0 and numFemalesHIV > 0:
                totalMalesHiv += numMalesHIV
                totalFemalesHiv += numFemalesHIV
    sexStatistics = {'malesHIV': totalMalesHiv, 'femalesHIV': totalFemalesHiv}
    return sexStatistics

                









