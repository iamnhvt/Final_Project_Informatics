google.charts.setOnLoadCallback(drawChart);

var malesGeoChart = [];
var femalesGeoChart = [];
var input = document.getElementById('b2');
var continentInput = document.getElementById('continent');
var malesButton = document.getElementById("malesButtonGeochart");
var femalesButton =document.getElementById("femalesButtonGeochart");
var currentData;

// When the user change the continet, 
// We then filter all the countries in that continent, and change the color scale
function createTableData(continent){

  // New Males and females geo chart data
  malesGeoChart = [];
  femalesGeoChart = [];

  // Iterate all year in the dictionary
  for (var key in yearData) {
      // Create headers for males and femlaes data
      var yearDataMales = [['Country', 'Males HIV incidence']];
      var yearDataFemales = [['Country', 'Females HIV incidence']];

      // Add just countries in that continent to the rows
      for (var i = 0; i < yearData[key].length; i++){
          if (yearData[key][i]['region'].toUpperCase().indexOf(continent.trim().toUpperCase()) == -1 && (continent != "" && continent != "World")) {
            continue;
          }
          var newrowMale = [];
          var newrowFemale = [];
          var curObject = yearData[key][i];
          // if (curObject['malesHIV'] > 3 || curObject['femalesHIV'] > 3)
          //   continue;
          newrowMale.push(curObject['countryName']);
          newrowMale.push(curObject['malesHIV']);
          newrowFemale.push(curObject['countryName']);
          newrowFemale.push(curObject['femalesHIV']);
          yearDataMales.push(newrowMale);
          yearDataFemales.push(newrowFemale);
      }
      malesGeoChart.push(yearDataMales);
      femalesGeoChart.push(yearDataFemales);
  }

  // Recreate the table data for the chart
  for (i = 0; i < malesGeoChart.length; i++){
      malesGeoChart[i] = google.visualization.arrayToDataTable(malesGeoChart[i]);
      femalesGeoChart[i] = google.visualization.arrayToDataTable(femalesGeoChart[i]);
  }

  // If males button is chosen, currentData is malesGeoChart. Otherwise, femalesGeoChart is chosen
  if (malesButton.className.indexOf("buttonActive") != -1)
    currentData = malesGeoChart;
  else
    currentData = femalesGeoChart;
}

function drawChart(){

  var chart = new google.visualization.GeoChart(document.getElementById('geochart'));
  createTableData("");

  // Set options for the geo chart
  var options = {
    region: 'world',
    colorAxis: {colors: ['#00853f', 'black', '#e31b23']},
    backgroundColor: '#81d4fa',
    datalessRegionColor: '#f8bbd0',
    defaultColor: '#f5f5f5'
  };

  
  // Get the current year
  var current = input.value;


  // Draw the geo chart
  function drawGeochart() {
      chart.draw(currentData[current], options);
  }

  drawGeochart();

  // If the user change the continent, change the chart
  continentInput.addEventListener('change', function(){
    var selectedContinent = continentInput.options[continentInput.selectedIndex].text;
    createTableData(selectedContinent);
    options['region'] = continentInput.options[continentInput.selectedIndex].value;
    drawGeochart();
  });


  // If the user change the year input, change the chart
  input.addEventListener('change', function(){
      current = parseInt(input.value);
      document.getElementById("currentYearGeochart").innerHTML = (1990 +current).toString();
      drawGeochart();
  });

  // when click on males button, redraw the chart following males data
  malesButton.addEventListener('click', function(){
      femalesButton.className = "buttonSlide";
      if (malesButton.className.indexOf("buttonActive") == -1)
          malesButton.className += " buttonActive";
      currentData = malesGeoChart;
      drawGeochart();
  });

  // when click on males button, redraw the chart following females data
  femalesButton.addEventListener('click', function(){
      malesButton.className = "buttonSlide";
      if (femalesButton.className.indexOf("buttonActive") == -1)
          femalesButton.className += " buttonActive";
      currentData = femalesGeoChart;
      drawGeochart();
  });
}