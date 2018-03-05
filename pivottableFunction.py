from flask import Flask, request, render_template, Markup
from collections import defaultdict
import numpy as np
import csv
import matplotlib
import matplotlib.cm as cm


'''
This python file defined all the function used in host.py
'''


'''observationdata compares two values using the compare value (derived from the form)
'''

def handlingErrors(rowLabel, columnLabel, filterSector, comparison, filterValue, operation, aggregatedSector):
    # If row label  = column label
    if (rowLabel == columnLabel):
        errorDescription = "Row Label and Column Label cannot be the same! Please Try again!"
        return True, errorDescription

    # If comparison is not choosing all values
    if (comparison != 9):
        if (filterValue == ""):
            errorDescription = "You have to input the Filter Value! Please try again!"
            return True, errorDescription
    
    # Cannot operate sum with percentage value
    if (aggregatedSector in ['malesHIV', 'femalesHIV'] and operation == 1):
        errorDescription = "Sum operation is not compatible with percentage value! Please try again!"
        return True, errorDescription

    # If there filter sector just contains string, the comparison must be compatible to string (7 and 8)
    if (filterSector in ['region', 'income'] and comparison not in [7, 8]):
        errorDescription = "Mathematical comparison is not compatible with string values! Please choose other comparisons!"
        return True, errorDescription

    if (filterSector not in ['region', 'income'] and comparison in [7, 8]):
        errorDescription = "String comparison is not compatible with numerical values! Please choose other comparisons!"
        return True, errorDescription

    # If there is no error, return false and "" (for error description)
    return False, ""


''' This function compares the value to the pivot value based on the compare value selected in form
'''
def compareData(filterValue, value, compare):
    if compare == 1:
        return (value > filterValue)
    elif compare == 2:
        return (value < filterValue)
    elif compare == 3:
        return (value >= filterValue)
    elif compare == 4:
        return (value <= filterValue)
    elif compare == 5:
        return (value != filterValue)
    elif compare == 6:
        return (value == filterValue)
    elif compare == 7:
        return (filterValue.strip().lower() in value.strip().lower())
    elif compare == 8:
        return (filterValue.strip().lower() not in value.strip().lower())
    else:
        return True #The last is all values


''' This function operates the aggregation operation on the data chose by users, then output all values in an array
'''
def aggregation(tableDict, operation):
    allDatas  = []
    columnLabels = set()

    for rLable in tableDict.keys():
        for columnLabel in tableDict[rLable]:
            columnLabels.add(columnLabel)
            data = tableDict[rLable][columnLabel]
            # Sum operation
            if operation == 1:
                tableDict[rLable][columnLabel] = np.around(sum(data), decimals = 2)
            # Average operation
            elif operation ==  2:
                tableDict[rLable][columnLabel] = np.around(sum(data)/(len(data)), decimals = 2)
            # Min operation
            elif operation == 3:
                tableDict[rLable][columnLabel] = np.around(min(data), decimals = 2)
            # Max operation
            elif operation == 4:
                tableDict[rLable][columnLabel] = np.around(max(data), decimals = 2)
            allDatas.append(tableDict[rLable][columnLabel])

    return allDatas, columnLabels


''' This functions creates all rows and headers to transfer to the value in pivottable.html (using render_template)
'''
def createHeadersRows(yearDict, allCountries, tableDict, operation, rowLabel, columnLabel):
    allDatas, columnLabels = aggregation(tableDict, operation)
    minData = min(allDatas)
    maxData = max(allDatas)


    #Create a color palttete for the data and color scale
    norm = matplotlib.colors.Normalize(vmin = minData, vmax = maxData, clip = True)
    mapper = cm.ScalarMappable(norm = norm, cmap = cm.RdBu_r)

    # Create color legends 
    colorLegends = []
    for rate in range(0, 1001, 15):
        value = minData + (maxData - minData) * rate / 1000.0
        rgba = mapper.to_rgba(value)
        colorLegends.append('rgba(%d, %d, %d, 0.5)' % (int(rgba[0]*255), int(rgba[1]*255), int(rgba[2] *255)))


    # Create headers for the table
    headers = [rowLabel.upper() + " \\ " + columnLabel.upper()]
    for columnLabel in sorted(columnLabels):
        headers.append(columnLabel)
    rows = []

    # Iterate Each cell in the table to find the colors of it in the selected scale
    for rLable in sorted(tableDict.keys()):
        newrow = [{'value': rLable, 'color': ''}]
        for columnLabel in sorted(columnLabels):
            # If there if data for column label
            if columnLabel in tableDict[rLable]:
                value = tableDict[rLable][columnLabel]
                rgba = mapper.to_rgba(value)
                # Append the value and corresponding value to the row
                newrow.append({'value': value, 'color': 'rgba(%d, %d, %d, 0.5)' % (int(rgba[0]*255), int(rgba[1]*255), int(rgba[2] *255))})
            else:
                # Apend empty value if the columnLabel does not have data
                newrow.append({'value': '', 'color': ''})
        rows.append(newrow)

    return headers, rows, colorLegends, minData, maxData

'''This functions create a dictionary in which:
+ Keys are all the value of row lable
+ Values are the dictionary in which:
    - Keys are all the value of column rowLabel
    - value is an array which contains all the value satisfied by filterSector and aggregatedSector

Finally this function will call createHeadersRows function to output the headers and rows to pass to pivottabel.html
'''
def createDynamicTable(yearDict, allCountries, rowLabel, columnLabel, filterSector, comparison, filterValue, operation, aggregatedSector):
    tableDict = {}
    
    # Iterate all country to find all suitable values
    for country in allCountries.keys():
        for year in allCountries[country]['statistics'].keys():
            
            rowLabelValue = allCountries[country][rowLabel] if rowLabel != 'year' else year
            columnLabelValue = allCountries[country][columnLabel] if columnLabel != 'year' else year
            if (rowLabelValue not in tableDict):
                tableDict[rowLabelValue] = defaultdict(list)
            
            # A set of statistics of current country of current year
            tmpData = allCountries[country]['statistics'][year]
           
            # A flag to indicate whether the value is satisfied with filterSector and comparison
            isOkData = False
            
             # If the filter is both for females and males HIV
            if filterSector == 'bothsex':
                isOkData =  compareData(filterValue, tmpData['malesHIV'], comparison) and \
                        compareData(filterValue, tmpData['femalesHIV'], comparison)
            else:
                # Else we just compare one filterSector
                if filterSector not in ['region', 'income']:
                    isOkData = compareData(filterValue, tmpData[filterSector], comparison)
                else:
                    isOkData = compareData(filterValue, allCountries[country][filterSector], comparison)

            # Add the data to current value of row label and column label
            if isOkData:
                # If aggregated Sector is for both sex, add all males and females to table
                if aggregatedSector == 'bothsex':
                    if (tmpData['malesHIV'] != 0):
                        tableDict[rowLabelValue][columnLabelValue].append(tmpData['malesHIV'])
                    if (tmpData['femalesHIV'] != 0):
                        tableDict[rowLabelValue][columnLabelValue].append(tmpData['femalesHIV'])
                else:
                    if (tmpData[aggregatedSector] != 0):
                        tableDict[rowLabelValue][columnLabelValue].append(tmpData[aggregatedSector])

    # Return the complete rows and headers format for the table
    return createHeadersRows(yearDict, allCountries, tableDict, operation, rowLabel, columnLabel)


'''This function dinamically creates description for values entered from the form
'''
def createDescription(operation, aggregatedSector, rowLabel, columnLabel, filterSector, comparison, filterValue):
    operations = ['', 'Sum of', 'Average of', 'Minimum of', 'Maximum of']
    comparisons = ['', '>', '<', '>=', '<=', '!=', '==', 'Contains', 'Does not contain', 'All values']
    description = ""
    description += '''%s <strong style = "color: #FF615C"> %s </strong>  by <strong style = "color: #7A90E8"> %s </strong>
                      and <strong style = "color: #7A90E8"> %s </strong>''' \
                      % (operations[operation], aggregatedSector, rowLabel, columnLabel)
    if comparison == 9:
        description += '''with all values of <strong style = "color: #FF615C">%s </strong>.''' % filterSector
    else:
        description += '''when <strong style = "color: #FF615C">%s </strong> %s %s.''' %(filterSector, comparisons[comparison], filterValue)

    # Return the Markup of description to display on the web
    return Markup(description.upper())

''' This functions creates headers and rows for general chart
'''
def createGeneralHeadersRows(allCountries):
    # Header of the table
    headers=['Country', 'Sign', 'Income Class', 'Region', 'average HIV Incidence (Females)', 
                'average HIV Incidence (Males)', 'Average Total GDP (billion $USD)', 'Average GDP Per Capita ($USD)', 'Average Population']
    rows = []

    # Check all country in the allCountries dictionary
    for country in allCountries.keys():
        # Create a row for the table. Since this is the general table, so there is no need for color value
        newrow = [{'value': unicode(country, errors='ignore'), 'color': ""}, 
                {'value': allCountries[country]['sign'], 'color':""},
                {'value': allCountries[country]['income'], 'color': ""},
                {'value': allCountries[country]['region'], 'color': ""}]

        # Sum statistics stores the average value for males, females HIV, total GDP, GDPPP, and population
        sumStatistics = defaultdict(int)
        for year in allCountries[country]['statistics']:
            for key, value in allCountries[country]['statistics'][year].items():
                if (value):
                    sumStatistics[key] += value
        # Calculate average (divided by the number of years, which is 26)
        # use numpy library to round the float value up to 2 decimals
        newrow.append({'value': np.around(sumStatistics['femalesHIV']/26.0, decimals = 2), 'color': ""})
        newrow.append({'value': np.around(sumStatistics['malesHIV']/26.0, decimals = 2), 'color': ""})
        newrow.append({'value': np.around(sumStatistics['totalGDP'], decimals = 2), 'color': ""})
        newrow.append({'value': np.around(sumStatistics['GDPPP']/26.0, decimals = 2), 'color': ""})
        newrow.append({'value': np.around(sumStatistics['population']/26.0, decimals = 2), 'color': ""})
        
        containEmpty = False

        # If the row contains 0 value, do not append it
        for obj in newrow:
            if not obj['value']:
                containEmpty = True
        if not containEmpty:
            rows.append(newrow)

    # Make the markup for the description to show on the web page
    description = Markup('''The average of all <strong style="color: #FF6D18"> STATISTICS </strong> <br> We collected throughout this project!''')
    return headers, rows, description

    


    