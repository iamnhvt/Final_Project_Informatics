
google.charts.load('upcoming', {
            'packages': ['corechart', 'geochart']
        });
google.charts.setOnLoadCallback(drawBubbleChart);

function drawBubbleChart() {
    // Set options for the bubble chart
    var options = {
        backgroundColor: "#fff",
        fontName: 'Georgia',
        hAxis: {
            title: 'GDP Per Capita ($)',
            gridlines: {
                count: 0
            },
            viewWindow: {
                max: '',
                min: '-1000'
            }
        },
        vAxis: {
            title: 'HIV incidence',
            gridlines: {
                count: 0
            },
            viewWindow: {
                min: '-1'
            }
        }, 
        bubble: {textStyle: {
            fontSize: 8,
            fontName: 'Georgia',
            color: 'none',
            },
            stroke: 'none',
            opacity: 0.5
        },
        animation: {
            duration: 500,
            easing: 'out',
            startup: true
        },
        legend: {
            position: 'right',
            maxLines: 1,
            alignment: 'center'
        },

        chartArea:{left: 100,top:10,width:'75%',height:'80%'},
        sizeAxis: {
            minSize: 15
        },
        series: {
            'East Asia and Pacific': {color: '#C83AE0'},
            'Middle East and North Africa': {color: '#22FCBB'},
            'Sub-Saharan Africa': {color: '#FC3E2C'},
            'Latin America and Caribbean': {color: '#F7D623'},
            'Europe and Central Asia': {color: '#2312E0'},
            'South Asia': {color: '#26Cf30'}
        },
        keepInBounds: true,
        explorer: { actions: ['dragToZoom', 'rightClickToReset'],
                    keepInBounds: true,
                    maxZoomIn: 8,
                    zoomDelta: 2
        }
        
    };

    // Create the valid rows of bubble chart data for males and females
    var malesBubbleChart = [];
    var femalesBubbleChart = [];
    for (var key in yearData) {
        var yearDataMales = [['Country', 'Total GDP', 'Males HIV incidence', 'Region', 'Population']];
        var yearDataFemales = [['Country', 'Total GDP', 'Females HIV incidence', 'Region', 'Population']];
        for (var i = 0; i < yearData[key].length; i++){
            // Create new tow for males and females
            var newrowMale = [];
            var newrowFemale = [];
            var curObject = yearData[key][i];

            // Push the data to males and females row
            newrowMale.push(curObject['countryName'] + "(" + curObject['sign'] +") - " + curObject['income']);
            newrowMale.push(curObject['GDPPP']);
            newrowMale.push(curObject['malesHIV']);
            newrowMale.push(curObject['region']);
            newrowMale.push(curObject['population']);
            newrowFemale.push(curObject['countryName'] + "(" + curObject['sign'] +") - " + curObject['income']);
            newrowFemale.push(curObject['GDPPP']);
            newrowFemale.push(curObject['femalesHIV']);
            newrowFemale.push(curObject['region']);
            newrowFemale.push(curObject['population']);
            yearDataMales.push(newrowMale);
            yearDataFemales.push(newrowFemale);
        }
        malesBubbleChart.push(yearDataMales);
        femalesBubbleChart.push(yearDataFemales);
    }

    // Change the data to valid forms
    for (i = 0; i < malesBubbleChart.length; i++){
        malesBubbleChart[i] = google.visualization.arrayToDataTable(malesBubbleChart[i]);
        femalesBubbleChart[i] = google.visualization.arrayToDataTable(femalesBubbleChart[i]);
    }

    // The current data to show on the web is males data
    var currentData = malesBubbleChart;

    // Get the id of div to show the chart
    var chart = new google.visualization.BubbleChart(
        document.getElementById('bubblechart'));

    // The the input element to change the year
    var input = document.getElementById('b1');

    // Get the GDP constraints to show on the chart
    var GDPConstraints = document.getElementById('GDPConstraints');

    // The the males and females button to change
    var malesButton = document.getElementById("malesButton");
    var femalesButton =document.getElementById("femalesButton");

    // Get the current year
    var current = input.value;
    
    function drawChart2() {
        // draw the chart
        chart.draw(currentData[current], options);
    }

    drawChart2();
    

    // The page will scroll to the chart when opening the page
    $('html, body').animate({ scrollTop: $('#chart1title').offset().top }, 'slow');
            
    // When the year change, redraw the chart
    input.addEventListener('change', function(){
        current = parseInt(input.value);
        document.getElementById("currentYear").innerHTML = (1990 +current).toString();
        drawChart2();
    });

    // When GDP constraint value changes, redraw the chart
    GDPConstraints.addEventListener('change', function(){
        options['hAxis']['viewWindow']['max'] = GDPConstraints.options[GDPConstraints.selectedIndex].value;
        options['hAxis']['viewWindow']['min'] = -GDPConstraints.options[GDPConstraints.selectedIndex].value/10;
        drawChart2();
    })
    

    // when click on males button, redraw the chart following males data
    malesButton.addEventListener('click', function(){
        femalesButton.className = "buttonSlide";
        if (malesButton.className.indexOf("buttonActive") == -1)
            malesButton.className += " buttonActive";
        currentData = malesBubbleChart;
        drawChart2();
    });

    // when click on females button, redraw the chart following females data
    femalesButton.addEventListener('click', function(){
        malesButton.className = "buttonSlide";
        if (femalesButton.className.indexOf("buttonActive") == -1)
            femalesButton.className += " buttonActive";
        currentData = femalesBubbleChart;
        drawChart2();
    });

}