var options = {
                title: 'Correlation between life expectancy, fertility rate ' +
               'and population of some world countries (2010)',
                

                fontName: 'Georgia',
                hAxis: {
                    title: 'Life Expectancy',
                    gridlines: {
                        count: 0
                    }
                },
                vAxis: {title: 'Fertility Rate'},
                bubble: {textStyle: {
                    fontSize: 8,
                    fontName: 'Georgia',
                    color: 'black',
                },
                    stroke: 'none'
                },
                animation: {
                    duration: 1000,
                    easing: 'out',
                    startup: true
                },
                // colorAxis: {
                //     colors: ['#FC5120', '#ffffff', '#3ef74c'],
                //     legend: {
                //         position: 'bottom',
                //         textStyle: {
                //         color: 'black',
                //         fontName: 'Georgia'
                //         }
                //     }
                // },
                legend: {
                    position: 'right',
                    alignment: 'center'
                },
                series: {
                    'North America': {color: '#c8B7f5'},
                    'Europe': {color: '#ffeeda'},
                    'Middle East': {color: '#92c791'}
                },
            };
            var rowData1 = [
            ['ID', 'Life Expectancy', 'Fertility Rate', 'Region',     'Population'],
            ['CAN',    80.66,              ,      'North America',  1],
            ['DEU',    79.84,              1.36,      'Europe',         2],
            ['DNK',    78.6,               1.84,      'Europe',         3],
            ['EGY',    72.73,              2.78,      'Middle East',    4],
            ['GBR',    80.05,              2,         'Europe',          5],
            ['IRN',    72.49,              1.7,       'Middle East',    6],
            ['IRQ',    68.09,              4.77,      'Middle East',    6],
            ['ISR',    81.55,              2.96,      'Middle East',    6],
            ['RUS',    68.6,               1.54,      'Europe',        8],
            ['USA',    78.09,              2.05,      'North America', 9]
             ];

            var rowData2 = [
            ['ID', 'Life Expectancy', 'Fertility Rate', 'Region',     'Population'],
            ['CAN',    83.66,              2.67,      'North America',  33739900],
            ['DEU',    52.84,              1.26,      'Europe',         81902307],
            ['DNK',    56.6,               1.04,      'Europe',         5523095],
            ['EGY',    72.73,              2.58,      'Middle East',    79716203],
            ['GBR',    85.05,              2,         'Europe',         61801570],
            ['IRN',    78.49,              1.5,       'Middle East',    73137148],
            ['IRQ',    82.09,              4.57,      'Middle East',    31090763],
            ['ISR',    89.55,              3.96,      'Middle East',    7485600],
            ['RUS',    75.6,               2.54,      'Europe',         141850000],
            ['USA',    89.09,              1.05,      'North America',  307007000]
             ];

            var rowData3 = [
            ['ID', 'Life Expectancy', 'Fertility Rate', 'Region',     'Population'],
            ['CAN',    80.66,              1.66,      'North America',  33739900],
            ['DEU',    59.84,              2.36,      'Europe',         81902307],
            ['DNK',    78.6,               1.84,      'Europe',         5523095],
            ['EGY',    42.73,              2.78,      'Middle East',    79716203],
            ['GBR',    80.05,              2,         'Europe',         61801570],
            ['IRN',    52.49,              1.7,       'Middle East',    73137148],
            ['IRQ',    68.09,              4.77,      'Middle East',    31090763],
            ['ISR',    81.55,              2.96,      'Middle East',    7485600],
            ['RUS',    68.6,               1.54,      'Europe',         141850000],
            ['USA',    78.09,              2.05,      'North America',  307007000]
             ];

             var rowData4 = [
            ['ID', 'Life Expectancy', 'Fertility Rate', 'Region',     'Population'],
            ['CAN',    850.66,              1.66,      'North America',  33739900],
            ['DEU',    29.84,              2.36,      'Europe',         81902307],
            ['DNK',    48.6,               1.84,      'Europe',         5523095],
            ['EGY',    22.73,              2.78,      'Middle East',    79716203],
            ['GBR',    20.05,              2,         'Europe',         61801570],
            ['IRN',    92.49,              1.7,       'Middle East',    73137148],
            ['IRQ',    78.09,              4.77,      'Middle East',    31090763],
            ['ISR',    71.55,              2.96,      'Middle East',    7485600],
            ['RUS',    68.6,               1.54,      'Europe',         141850000],
            ['USA',    58.09,              2.05,      'North America',  307007000]
             ];

            var data = [];

            data[0] = google.visualization.arrayToDataTable(rowData1);
            data[1] = google.visualization.arrayToDataTable(rowData2);
            data[2] = google.visualization.arrayToDataTable(rowData3);

            var currentData = data;
            var data0 = data;
            var data1 = [];
            data1[0] = google.visualization.arrayToDataTable(rowData1);
            data1[1] = google.visualization.arrayToDataTable(rowData2);
            data1[2] = google.visualization.arrayToDataTable(rowData4);


            var chart1 = new google.visualization.BubbleChart(
                document.getElementById('malesChart'));
            
            var input1 = document.getElementById('b1');
            var buttonMale = document.getElementById("malesButton");
            var buttonFemale = document.getElementById("femalesButton");

            var current = 0;
            function drawChart2() {
                // Disabling the button while the chart is drawing.
                //button.disabled = true;
                chart1.draw(currentData[current], options);
            }

            drawChart2();

            input1.addEventListener('change', function(){
                current = input1.value;
                drawChart2();
            });

            buttonMale.addEventListener('click', function(){
                currentData = data1;
                drawChart2();
            })

            buttonFemale.addEventListener('click', function(){
                currentData = data0;
                drawChart2();
            });