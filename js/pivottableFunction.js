// This js file describes all the functions used in pivot table site

// This functions checks if n is numerical or not
function isNumeric(n){
        return !isNaN(parseFloat(n)) && isFinite(n);
}

//Sort the table following the column index (using bubble sort)
function sort(columnIndex) {
    //Get tbody and thead of the table
    var tbody = document.getElementById("pTable").getElementsByTagName("tbody")[0];
    var thead = document.getElementById("pTable").getElementsByTagName("thead")[0];

    // Get the all the headings of the table
    var heading = thead.getElementsByTagName("th");

    // Get all the rows of table body
    var rows = tbody.getElementsByTagName("tr");

    // Get the current status of the current column index that needed to sort
    var columnClass = heading[columnIndex].className;

    // If this column is unsorted or is sorted in descending order, sort in in ascending order
    if (columnClass == "unsorted" || columnClass == "descending"){
        ascending = true;

        // Change the class and glyphincon to ascending
        heading[columnIndex].className = "ascending";
        heading[columnIndex].getElementsByTagName("span")[0].className = "glyphicon glyphicon-sort-by-attributes";

        // Make the other columns to be unsorted
        for (i = 1; i < heading.length; i++){
            if (i != columnIndex){
                heading[i].className = "unsorted";
                heading[i].getElementsByTagName("span")[0].className = "glyphicon glyphicon-sort";
            }
        }
    } else { // If the column is ascending, change status to descending
        ascending = false;
        heading[columnIndex].className = "descending";
        heading[columnIndex].getElementsByTagName("span")[0].className = "glyphicon glyphicon-sort-by-attributes-alt";

        for (i = 1; i < heading.length; i++)
            if (i != columnIndex){
                heading[i].className = "unsorted";
                heading[i].getElementsByTagName("span")[0].className = "glyphicon glyphicon-sort";
            }
    }


    var unsorted = true;

    // THe main function of bubble chart, sort the column index in required order
    while (unsorted) {
        unsorted = false

        for (var r = 0; r < rows.length - 1; r++) {
            var row = rows[r];
            var nextRow = rows[r + 1];

            var value = row.getElementsByTagName('td')[columnIndex].innerHTML;
            var nextValue = nextRow.getElementsByTagName('td')[columnIndex].innerHTML;

            if (isNumeric(value)){
                value = parseFloat(value);
                nextValue = parseFloat(nextValue);
            }
            
            if (ascending ? value > nextValue : value < nextValue) {
                tbody.insertBefore(nextRow, row);
                unsorted = true;
            }   
        }
    }

    // Recreate the no. for each row
    for (i = 0; i < rows.length; i++){
        rows[i].getElementsByTagName("td")[0].innerHTML = i + 1;
    }

    // Finally, show the page in the new order
    showPage(parseInt(document.getElementById("currentPage").value));

    //If there is find Value in the searchBar, find it in the sorted order
    findValue();
}


// Show the current page 
function showPage(pageNumber){
    var tbody = document.getElementById("pTable").getElementsByTagName("tbody")[0];
    var rows = tbody.getElementsByTagName("tr");
    document.getElementById("currentPage").value = pageNumber;
    var rowsPerPage = document.getElementById("rowsPerPage").value;
    for (i = 0; i < rows.length; i++){
        rows[i].style.display = 'none';
    }
    for (i = (pageNumber-1) * rowsPerPage; i < Math.min(pageNumber * rowsPerPage, rows.length); i++){
        rows[i].style.display = "table-row";
    }
}


// Increase the number of page by num
function plusPage(num){
    var tbody = document.getElementById("pTable").getElementsByTagName("tbody")[0];
    var rows = tbody.getElementsByTagName("tr");
    var rowsPerPage = document.getElementById("rowsPerPage").value;
    var currentPage = parseInt(document.getElementById("currentPage").value);

    if (currentPage + num > Math.ceil(rows.length / rowsPerPage) || currentPage + num <= 0)
        return;
    currentPage += num;

    showPage(currentPage);
}


// Find all the row that matches the input country
function findValue(){
    var tbody = document.getElementById("pTable").getElementsByTagName("tbody")[0];
    var thead = document.getElementById("pTable").getElementsByTagName("thead")[0];

    var heading = thead.getElementsByTagName("th");
    var rows = tbody.getElementsByTagName("tr");

    var rowsPerPage = document.getElementById("rowsPerPage").value;
    var currentPage = parseInt(document.getElementById("currentPage").value);
    var valueInput = document.getElementById("countryInput").value.toUpperCase();
    var inputSearchColumn = document.getElementById("searchColumn").value;

    // If the user inputs a valid column index
    if (isNumeric(inputSearchColumn)){
        inputSearchColumn = parseInt(inputSearchColumn);
        // Change the color status of selected index, and repaint the others
        for (i = 0; i < heading.length; i++){
            heading[i].style.background = "#1b1e24";
        }

        // If column index in not in range of the table, return the function
        if (inputSearchColumn <= 0 || inputSearchColumn > heading.length){
            return;
        }

        // Make the selected column a distinct color
        heading[inputSearchColumn - 1].style.background = "#828384";

        if (! valueInput) {
            showPage(document.getElementById("currentPage").value);
            return;
        }

        // Iterate all rows to find the row has the required value
        for (i = 0; i < rows.length; i++){
            var countryRow = rows[i].getElementsByTagName("td")[inputSearchColumn - 1].innerHTML.toUpperCase();
            if (countryRow.indexOf(valueInput) > -1) {
                rows[i].style.display = "table-row";
            } else {
                rows[i].style.display = "none";
            }
        }
    } else {
        // If the user input the wrong value for column, reset color for all columns
        for (i = 0; i < heading.length; i++){
            heading[i].style.background = "#1b1e24";
        }
    }
}


// Show the first page of the table
showPage(1);


// This function dynamically draws bar char corresponding the generated table
function drawPivotChart(){

    // Initalize the google API for bar chat
    document.getElementById("pivotChartWrapper").style.display = "inline-block";
    $('html, body').animate({ scrollTop: $('#pivotChart').offset().top }, 'slow');
    google.charts.load('current', {'packages':['bar']});
    google.charts.setOnLoadCallback(drawBarChart);


    // This functions draws the bar chart
    function drawBarChart(){

        // Get the main information of the pivot table
        var tbody = document.getElementById("pTable").getElementsByTagName("tbody")[0];
        var thead = document.getElementById("pTable").getElementsByTagName("thead")[0];
        var headings = thead.getElementsByTagName("th");
        var rowDatas = tbody.getElementsByTagName("tr");
        var rows = [];

        // Split the title of the table to make hAxis and vAxis title
        var title = headings[1].getElementsByTagName("p")[0].innerHTML.split("\\");
        var hTitle = title[0];
        var vTitle = title[1];

        // Initialize the characteristics of the bar chart
        var options = {
            title: "BAR CHART REPRESENTING THE ABOVE PIVOT TABLE",
            titleTextStyle: {
                color: "#23A7E8",
                fontSize: 20
            },
            subtitle: hTitle + "GROUP VERSUS" + vTitle + "GROUP",
            backgroundColor: "#F2F2F2",
            chartArea: {
                backgroundColor: '#F2F2F2',
                width: '90%',
                height: '75%',
                top: 0
            },
            bars: 'vertical',
            vAxis: {
                title: vTitle,
                titleTextStyle: {
                    fontSize: 20,
                    bold: 'true',
                    fontColor: "#929292"
                },
                gridlines: {
                    color: 'transparent'
                }
            },
            hAxis: {
                title: hTitle,
                textStyle : {
                    fontSize: 9
                },
                titleTextStyle: {
                    fontSize: 20,
                    bold: 'true',
                    fontColor: "#929292"
                }
            },
            legend: {
                position: 'top',
                maxLines: 3,
                alignment: 'center'
            }
        };

        // Create the first row of the barchart data, which is the header
        var header = [];
        //Ignore the heading of first and second column
        for (i = 1; i < headings.length; i++){
            var currentHead = headings[i].getElementsByTagName("p")[0].innerHTML;
            header.push(currentHead);
        }
        rows.push(header);


        // Add each data corresponding to the headers to the final rows
        for (i = 0; i < rowDatas.length; i++){
            var currentRow = rowDatas[i].getElementsByTagName("td");
            var tmpRow = [currentRow[1].innerHTML];
            for (j = 2; j < currentRow.length; j++)
                tmpRow.push(Number((parseFloat(currentRow[j].innerHTML)).toFixed(4)));
            rows.push(tmpRow);
        }

        // Create a data of googel chart generated by the rows 
        var data  = google.visualization.arrayToDataTable(rows);

        // Get the element of div to show the chart
        var chart = new google.charts.Bar(document.getElementById('pivotChart'));

        // Draw the chart
        chart.draw(data, google.charts.Bar.convertOptions(options));
    }
}


// This functions dynamically switch the current rows and columns of the chart
// in order to make it more flexible to users
function switchRowColumn(){
    $('html, body').animate({ scrollTop: $('#pTable').offset().top }, 'slow');
    var tbody = document.getElementById("pTable").getElementsByTagName("tbody")[0];
    var thead = document.getElementById("pTable").getElementsByTagName("thead")[0];
    var headRows = thead.getElementsByTagName("tr")[0];
    var headings = headRows.getElementsByTagName("th");
    var rowDatas = tbody.getElementsByTagName("tr");


    // New rows is the new table data
    var newRows = new Array(headings.length -2);

    // Initialize the headings for new table
    for (var i = 0; i < newRows.length; i++){
        newRows[i] = new Array(rowDatas.length + 2);
        newRows[i][0] = {'value': i + 1, 'color': ""};
        var currentHeading = headings[i+2].getElementsByTagName("p")[0].innerHTML;
        newRows[i][1] = {'value': currentHeading, 'color': ""};
    }

    var rowColumnHeading = headings[1].getElementsByTagName("p")[0].innerHTML;


    var deletedRow = [];
    var newHeaders = [];
    for (var i = 0; i < rowDatas.length; i++){
        var currentRow = rowDatas[i].getElementsByTagName("td");
        newHeaders.push(currentRow[1].innerHTML);
        deletedRow.push(rowDatas[i]);
        for (var j = 2; j < currentRow.length; j++){
            newRows[j -2 ][i + 2] = {'value': currentRow[j].innerHTML, 'color': currentRow[j].style.background}
        }
    }

    var deleted = []

    for (var i = 2 + rowDatas.length; i < headings.length; i++){
        var currentHeading = headings[i];
        deleted.push(currentHeading);
    }

    for (var i = 0; i < deleted.length; i++)
        deleted[i].parentNode.removeChild(deleted[i]);
    for (var i = 0; i < deletedRow.length; i++)
        deletedRow[i].parentNode.removeChild(deletedRow[i]);
    
    var title = headings[1].getElementsByTagName("p")[0].innerHTML.split("\\");
    var hTitle = title[0];
    var vTitle = title[1];
    headings[1].getElementsByTagName("p")[0].innerHTML = vTitle + "\\" + hTitle;

    for (var i = headings.length - 2; i < newHeaders.length; i++){
        var newHeader = document.createElement("th");
        newHeader.appendChild(document.createElement("p"));

        var div = document.createElement("div");
        div.className = "sortSign";
        var span = document.createElement("span");
        span.className = "glyphicon glyphicon-sort";
        div.appendChild(span);

        newHeader.appendChild(div);
        headRows.append(newHeader);
    }

    for (var i = 0; i < newHeaders.length; i++){
        headings[i+2].getElementsByTagName("p")[0].innerHTML = newHeaders[i];
    }

    for (var i = 0; i < newRows.length; i++){
        var rowElement = document.createElement("tr");
        for (var j = 0; j < newRows[i].length; j++){
            var tdElement = document.createElement("td");
            tdElement.style.background = newRows[i][j]['color'];
            tdElement.innerHTML = newRows[i][j]['value'];
            rowElement.appendChild(tdElement);
        }
        tbody.appendChild(rowElement);
    }
}