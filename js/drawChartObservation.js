google.charts.load('current', {'packages':['line', 'corechart', 'bar']});
google.charts.setOnLoadCallback(drawYearHivChart);
google.charts.setOnLoadCallback(drawHivRegionChart);
google.charts.setOnLoadCallback(drawHivIncomeChart);
google.charts.setOnLoadCallback(drawHivPopulationChart);
google.charts.setOnLoadCallback(drawMalesVsFemalesChart);

// Year vs HIV Chart
function drawYearHivChart(){        
    // Initialize the characteristics of the Line chart
    var options = {
        fontSize: 18,
        chart: {
          title: 'Year vs Percentage of HIV Incidence',
          titlePosition: 'out',
          subtitle: 'Across The Period of 1990 to 2015'
        },
        legend: {
            textStyle: {
                fontSize: 11
            }
        }
    };

    // Create the valid rows for google chart API
    var data = new google.visualization.DataTable();
    // Add columns to the table
    data.addColumn('string', 'Year');
    data.addColumn('number', 'HIV Males Incidence');
    data.addColumn('number', 'HIV Females Incidence');
    data.addColumn('number', 'HIV Incidence (Both Sex)');
    rows = []
    for (var key in hiv_vs_year_data)
    {
        var row = [key, hiv_vs_year_data[key]['males'], hiv_vs_year_data[key]['females'], hiv_vs_year_data[key]['bothSex']];
        rows.push(row); 
    }

    // Add all the rows to the Data Table
    data.addRows(rows);

    // Get Element of the div and Draw the chart
    var chart = new google.charts.Line(document.getElementById('year_vs_HIV'));
    chart.draw(data, google.charts.Line.convertOptions(options));
}


// Region vs HIV Chart
function drawHivRegionChart(){
    // Initialize the characteristics of the Pie chart
    var options = {
        pieHole: 0.4,
        fontSize: 18,
        
        title: 'Region vs Average Percentage of HIV Incidence (Both Sex) (1990-2015)',
        titleTextStyle: {
            color: "#9A9A9A"
        },
        legend: {
            alignment: 'center',
            textStyle: {
                fontSize: 11
            }
        }
    };

    // Create the valid rows for google chart API
    var data = new google.visualization.DataTable();
    // Add columns to the table
    data.addColumn('string', 'Region');
    data.addColumn('number', 'Average HIV Incidence');
    var rows = [];
    for (var key in hiv_vs_region_data){
        var row = [key, hiv_vs_region_data[key][0]];
        rows.push(row);
    }

    // Add all the rows to the Data Table
    data.addRows(rows);


    // Get Element of the div and Draw the chart
    var chart = new google.visualization.PieChart(document.getElementById('hiv_vs_region'));
    chart.draw(data, options);
}


function drawHivIncomeChart(){
    // Initialize the characteristics of the Pie chart
    var options = {
        pieHole: 0.4,
        fontSize: 18,
        
        title: 'Income Class vs Average Percentage of HIV Incidence (Both Sex) (1990-2015)',
        titleTextStyle: {
            color: "#9A9A9A"
        },
        legend: {
            alignment: 'center',
            textStyle: {
                fontSize: 11
            }
        }
    };

    // Create the valid rows for google chart API
    var data = new google.visualization.DataTable();
    // Add columns to the table
    data.addColumn('string', 'Region');
    data.addColumn('number', 'Average HIV Incidence');
    var rows = [];
    for (var key in hiv_vs_income_data){
        var row = [key, hiv_vs_income_data[key][0]];
        rows.push(row);
    }

    // Add all the rows to the Data Table
    data.addRows(rows);

    // Get Element of the div and Draw the chart
    var chart = new google.visualization.PieChart(document.getElementById('hiv_vs_income'));
    chart.draw(data, options);
}

function drawHivPopulationChart(){
    // Initialize the characteristics of the bar chart
    var options = {
        fontSize: 18,
        title: "Population Class vs Average Percentage of HIV Incidence (Both Sex) (1990-2015)",
        titlePosition: 'out',
        bars: 'horizontal',
        legend: {
            position: 'right',
            alignment: 'center',
            textStyle: {
                fontSize: 11
            }
        }
    };

    // Create the valid rows for google chart API
    var data = new google.visualization.DataTable();
    // Add columns to the table
    data.addColumn('string', 'Population Class');
    data.addColumn('number', 'HIV Males Incidence');
    data.addColumn('number', 'HIV Females Incidence');
    var rows = [];
    var mainKey = ['Lower Population', 'Low Population', 'Middle Population', 'Upper Middle Population', 'High Population'];
    var info = ['<1M', '<10M', '<30M', '<80M', '>=80M'];
    for (i = 0; i < mainKey.length; i++){
        var key = mainKey[i];
        var key2 = key + '(' + info[i] + ')';
        var row = [key2, hiv_vs_population_data[key][0][0], hiv_vs_population_data[key][0][1]];
        rows.push(row);
    }

    // Add all the rows to the Data Table
    data.addRows(rows);


    // Get the element of div to show the chart
    var chart = new google.charts.Bar(document.getElementById('hiv_vs_population'));

    // Draw the chart
    chart.draw(data, google.charts.Bar.convertOptions(options));
}


// Males vs Females Pie Chart
function drawMalesVsFemalesChart(){
    // Initialize the characteristics of the Pie chart
    var options = {
        pieHole: 0.4,
        fontSize: 18,
        
        title: 'Number of Males Vs Females With HIV (1990-2015)',
        titleTextStyle: {
            color: "#9A9A9A"
        },
        legend: {
            alignment: 'center'
        },
        chartArea: {
            width: 450,
            height: 400
        }
    };

    // Create the valid rows for google chart API
    var data = new google.visualization.DataTable();
    // Add columns to the table
    data.addColumn('string', 'Sex');
    data.addColumn('number', 'Number of HIV Incidence');
    data.addRows([
        ['Males', sexStatistics['malesHIV']],
        ['Females', sexStatistics['femalesHIV']]
    ])

    // Add all the rows to the Data Table



    // Get Element of the div and Draw the chart
    var chart = new google.visualization.PieChart(document.getElementById('males_vs_females'));
    chart.draw(data, options);
}


