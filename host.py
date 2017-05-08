from flask import Flask, request, render_template
from collections import defaultdict
import numpy as np
import csv
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


app = Flask(__name__, static_folder='.', static_url_path='')

def readData():
    fileIn = open('data.csv')
    data = list(csv.reader(fileIn))
    return data

def addRowTable(line):
    row = ''
    row += "['%s'," % line[0].strip()
    row += "'%s'," % line[1].strip()
    row += "{v: %d, f: '$%d'}," % (int(line[2]), int(line[2]))
    row += "%s]" % ('true' if line[3] == 'yes' else 'false')
    return row

def cleanData(fileData):
    for i in range(len(fileData)):
        if (not fileData[i]):
            del(fileData[i])

    for line in fileData:
        for  i in range(len(line)):
            line[i] = line[i].strip()

def getData():
    femalesHIVFile = open('data/femalesHIV.csv')
    femalesHIVData = list(csv.reader(femalesHIVFile))[4:]

    malesHIVFile = open('data/malesHIV.csv');
    malesHIVData = list(csv.reader(malesHIVFile))[4:]

    totalGDPFile = open("data/totalGDP.csv")
    totalGDPData = list(csv.reader(totalGDPFile))[4:]

    GDPPFile = open("data/GDPPP.csv")
    GDPPData = list(csv.reader(GDPPFile))[4:]

    populationFile = open("data/population.csv")
    populationData = list(csv.reader(populationFile))[4:]

    regionFile = open("data/region.csv")
    regionData = list(csv.reader(regionFile))

 

    # Delete empty rows
    cleanData(femalesHIVData)
    cleanData(malesHIVData)
    cleanData(totalGDPData)
    cleanData(GDPPData)
    cleanData(regionData)

    yearDict = {}
    signDictionary = {}
    allCountries = {}

    # Add females HIV data to each country for each year
    for row in femalesHIVData[1:]:
        # Assign the name of the country to its sign
        signDictionary[row[1]] = row[0]

        # Iterate all the years
        for i in range(4, len(femalesHIVData[0])):
            # If the data is empty, do not process it
            if (not row[i]):
                break
            currentYear = femalesHIVData[0][i]

            # If the current year has been not processed yet, create a dictionary as a value for it
            if currentYear not in yearDict:
                yearDict[currentYear] = {}

            # If the country has been not processed yet, create a dictionary as a value for it
            if row[0] not in yearDict[currentYear]:
                yearDict[currentYear][row[0]] = {}
            
            yearDict[currentYear][row[0]]["femalesHIV"] = float(row[i])

    # Add males HIV data to each country for each year
    for row in malesHIVData[1:]:
        for i in range(4, len(malesHIVData[0])):
            if (not row[i]):
                break

            currentYear = malesHIVData[0][i]
            
            if row[0] in yearDict[currentYear]:
                yearDict[currentYear][row[0]]["malesHIV"] = float(row[i])
            

    # Add toal GDP data to each country for each year
    for row in totalGDPData[1:]:
        for i in range(4, len(totalGDPData[0])):
            if (not row[i]):
                row[i] = 0
            currentYear = totalGDPData[0][i]
            if currentYear not in yearDict:
                continue
            
            if row[0] in yearDict[currentYear]:
                yearDict[currentYear][row[0]]["totalGDP"] = float(row[i])

    # Add GDPPP data to each country for each year
    for row in GDPPData[1:]:
        for i in range(4, len(GDPPData[0])):
            if (not row[i]):
                row[i] = 0
            currentYear = GDPPData[0][i]
            if currentYear not in yearDict:
                continue
            
            if row[0] in yearDict[currentYear]:
                yearDict[currentYear][row[0]]["GDPPP"] = float(row[i])
            

    # Add population data to each country for each year
    for row in populationData[1:]:
        for i in range(4, len(populationData[0])):
            if (not row[i]):
                row[i] = 0
            currentYear = populationData[0][i]
            if currentYear not in yearDict:
                continue
            
            if row[0] in yearDict[currentYear]:
                yearDict[currentYear][row[0]]["population"] = float(row[i])
            

    # Find all unique countries
    for year in range(1990, 2016):
        for country in yearDict[str(year)]:
            allCountries[country] = {}

    # for year in range(1990, 2016):
    #     for country in allCountries.keys():
    #         # Info for each country of each year
    #         infoC = yearDict[str(year)][country]
    #         # If there is no statistic about HIV, delete that country
    #         if infoC["malesHIV"] == infoC["femalesHIV"] == -1:
    #             del yearDict
    
    # Add region, sign, and income type for each country
    for line in regionData[1:]:
        if line[0] in signDictionary:
            country = signDictionary[line[0]]
            if country in allCountries:  
                allCountries[country]['sign'] = line[0] 
                allCountries[country]['region'] = line[1]
                allCountries[country]['income'] = line[2]

    #Delete all the surplus areas, which no not have specific region
    surplusArea = []
    for country in allCountries:
        if (not allCountries[country]['region']):
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


@app.route('/bubblechart.html', methods=['GET'])
def bubblechart():
    yearDict, allCountries = getData()
    rows = []
    for year in sorted(yearDict.keys()):
        newrows = []
        for country in allCountries.keys():
            if country not in yearDict[year]:
                continue
            newobject = {}
            newobject["sign"] = allCountries[country]['sign']
            newobject["region"] = allCountries[country]['region']
            newobject["income"] = allCountries[country]["income"]
            newobject["countryName"] = country.strip().decode('cp1252').encode('utf-8')
            newobject["totalGDP"] = float(yearDict[year][country]['GDPPP'])
            newobject["femalesHIV"] = float(yearDict[year][country]["femalesHIV"])
            newobject["malesHIV"] = float(yearDict[year][country]["malesHIV"])
            newobject["population"] = float(yearDict[year][country]["population"])
            newrows.append(newobject)
        rows.append(newrows)

    return render_template("chart2.html", rows = rows, countries = allCountries)


@app.route('/form.html', methods=['GET'])
def form():
    return render_template('form.html')

@app.route('/pivottable.html', methods=['GET', 'POST'])
def pivotTable():
    if request.method == 'GET':
        yearDict, allCountries = getData()
        headers=['Country', 'Sign', 'Income Class', 'Region', 'average HIV Incidence (Females)', 
                'average HIV Incidence (Males)', 'Average Total GDP (billion $USD)', 'Average GDP Per Capita ($USD)', 'Average Population']
        rows = []
        for country in allCountries.keys():
            newrow = [country, allCountries[country]['sign'], allCountries[country]['income'],
                      allCountries[country]['region']]

            sumStatistics = defaultdict(int)
            for year in allCountries[country]['statistics']:
                for key, value in allCountries[country]['statistics'][year].items():
                    if (value):
                        sumStatistics[key] += value
            newrow.append(np.around(sumStatistics['femalesHIV']/26, decimals = 2))
            newrow.append(np.around(sumStatistics['malesHIV']/26, decimals = 2))
            newrow.append(np.around(sumStatistics['totalGDP']/(26*(10**9)), decimals = 2))
            newrow.append(np.around(sumStatistics['GDPPP']/26, decimals = 2))
            newrow.append(np.around(sumStatistics['population']/26, decimals = 2))
            rows.append(newrow)

        return render_template('pivottable copy.html', headers = headers, rows = rows)

    if request.method == 'POST':
        minSalary = int(request.form['minSalary'])
        maxSalary = int(request.form['maxSalary'])
        country = request.form['country'].strip().lower()
        isFullTime = request.form['isFullTime']
        dataCSV = readData()
        filterData = [[line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip()] for line in dataCSV if int(line[2]) in range(minSalary, maxSalary + 1)\
        and line[1].strip().lower() == country and (isFullTime == 'both' or line[3].strip() == isFullTime)]
        rows = []
        for line in filterData:
            object = {}
            object['name'] = line[0]
            object['country'] = line[1]
            object['salary'] = line[2]
            object['isFullTime'] = True if line[3] =='yes' else False
            rows.append(object)
        
        return render_template('pivottable copy.html', rows = rows)

@app.route('/')
def main():
    rows = [
        {
            'name': 'meo',
            'country': 'VN',
            'salary': '20000'
        },
        {
            'name': 'tram',
            'country': 'vn',
            'salary': '200000'
        }
    ]
    return render_template("pivottable.html", rows = rows)

if __name__ == "__main__":
    app.run(debug=True)


