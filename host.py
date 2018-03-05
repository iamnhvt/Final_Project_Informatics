from flask import Flask, request, render_template, Markup
from collections import defaultdict
import numpy as np
import csv
import json
import matplotlib
import codecs
import matplotlib.cm as cm

import pivottableFunction
import dataProcessing
import observationData

app = Flask(__name__, static_folder='.', static_url_path='')

# Get the two dictionary which stores all the data read
yearDict, allCountries = dataProcessing.getData()


# General Chart Page
@app.route('/generalChart.html', methods=['GET'])
def bubblechart():
    # Create a general diction to pass to generalChart page
    years = {}

    # Iterate all years
    for year in sorted(yearDict.keys()):
        years[year] = []
        # Iterate all the country
        for country in allCountries.keys():
            # If the country not in yearDict, try another country
            if country not in yearDict[year]:
                continue
            # Otherwise, add all informations to the dictionary
            newobject = {}
            newobject["sign"] = allCountries[country]['sign']
            newobject["region"] = allCountries[country]['region']
            newobject["income"] = allCountries[country]["income"]
            newobject["countryName"] = unicode(country, errors = 'ignore')
            newobject["totalGDP"] = float(yearDict[year][country]['totalGDP'])
            newobject["GDPPP"] = float(yearDict[year][country]['GDPPP'])
            newobject["femalesHIV"] = float(yearDict[year][country]["femalesHIV"])
            newobject["malesHIV"] = float(yearDict[year][country]["malesHIV"])
            newobject["population"] = float(yearDict[year][country]["population"])

            containEmpty = False

            # If there is one zero values, the bubble charts cannot show that country, so dont append it
            for value in newobject.values():
                if (not value):
                    containEmpty = True
            if not containEmpty:
                years[year].append(newobject)

    # Create a JSON file which includes the year dictionary
    with open('generatedData/yearData.json', 'w') as outfile:
        json.dump(years, outfile)


    return render_template("generalChart.html")

# Pivot Table Form Page
@app.route('/form.html', methods=['GET'])
def form():
    return render_template('form.html')


# Observation page
@app.route('/observation.html', methods = ['GET'])
def observation():
    # Get the four set of data from observationData.py
    year_vs_HIV = observationData.hiv_vs_year(yearDict)
    hiv_vs_region = observationData.hiv_region(allCountries, yearDict)
    hiv_vs_income = observationData.income_v_hiv(allCountries, yearDict)
    hiv_vs_populaltion = observationData.hiv_vs_population(allCountries, yearDict)
    sexStatistics = observationData.male_vs_females(allCountries, yearDict)

    # Generate 4 corresponding json file to create 4 charts
    with open('generatedData/hiv_vs_year.json', 'w') as outfile:
        json.dump(year_vs_HIV, outfile)

    with open('generatedData/hiv_vs_region.json', 'w') as outfile:
        json.dump(hiv_vs_region, outfile)

    with open('generatedData/hiv_vs_income.json', 'w') as outfile:
        json.dump(hiv_vs_income, outfile)

    with open('generatedData/hiv_vs_population.json', 'w') as outfile:
        json.dump(hiv_vs_populaltion, outfile)

    with open('generatedData/males_vs_females.json', 'w') as outfile:
        json.dump(sexStatistics, outfile)

    return render_template('observation.html')

# Pivot table page
@app.route('/pivottable.html', methods=['GET', 'POST'])
def pivotTable():
    # If there is no required value for pivot table, show the general value on the pivot table
    if request.method == 'GET':
        # Get the headers, rows,and description from the function on pivottableFunction.py
        headers, rows, description = pivottableFunction.createGeneralHeadersRows(allCountries)
        return render_template('pivottable.html', headers = headers, rows = rows, description = description)
    else:
        # If there is filter value for the pivot table, get the value by request (from flask)
        rowLabel = request.form['rowLabel']
        columnLabel = request.form['columnLabel']
        filterSector = request.form['filterSector']
        comparison = int(request.form['comparison'])

        # If the user input float value, parse it to float
        try:
            filterValue = float(request.form['filterValue'])
        except ValueError: # Otherwise, keep the original form
            filterValue = request.form['filterValue']
        operation = int(request.form['operation'])
        aggregatedSector = request.form['aggregatedSector']

        # Check if there is any errors when user input the value
        isError, errorDescription = pivottableFunction.handlingErrors(rowLabel, columnLabel, filterSector, comparison, filterValue, operation, aggregatedSector)

        # If there is error, show the error handlings page
        if (isError):
            return render_template('pivottable.html', errors = isError, description = errorDescription)
        else:
            # Otherwise, create the rows, headers, and description and create a table
            description = pivottableFunction.createDescription(operation, aggregatedSector, rowLabel, columnLabel,
                                                                              filterSector, comparison, filterValue)

            headers, rows, colorLegends, minData, maxData = pivottableFunction.createDynamicTable(yearDict, allCountries, rowLabel, columnLabel, filterSector, comparison, filterValue, operation, aggregatedSector)
            
            return render_template('pivottable.html', headers = headers, rows = rows, description = description,\
                                                         errors = isError, colorLegends = colorLegends, minData = minData, maxData = maxData)

@app.route("/huhu.html")
def huhu():
    return render_template('huhu.html')

# Home page
@app.route('/')
@app.route('/home.html')
def main():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)


