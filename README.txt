———————Final Project - Foundations of Informatics - Sem 1 —————
Video for usage: https://www.youtube.com/watch?v=EKTj8uss6jg
Title: Collections Of HIV Data Around The World In The Period of 1990 to 2015
	Readme File
	May 22 2017
———————————————————————————————-———————————————————————————————-
CONTENTS
———————————————————————————————-———————————————————————————————-
1. INTRODUCTION AND PREQUISITE
2. DATA SOURCE
3. DATA PROCESSING
4. STRUCTURE OF THE WEB PLATFORM
	4.1. FRAMEWORK, OUTSOURCED LIBRARY AND API
	4.2. WEB STRUCTURE
	4.3 SUPPORTED FUNCTION (JS & PY FILE)
5. FOLDER STRUCTURE
6. HOW TO RUN THE WEB
7. REFERENCE

————————————————————————————————————
1. INTRODUCTION AND PREQUISITE
————————————————————————————————————
This web platform is the 12-week project of the subject Foundations of Informatics. The website mainly focuses on the HIV statistics and information around the world. Particularly, the data is collected from a number of sources (described in section 2), then it will be processed by  Python at server side. After the data is analyzed and useful information is discovered, it will be sent to the presentation layer (front-end) in order to display the information to the users and provide them with many features to get the information they require. 

In order to let this platform run successfully in your computer, you have to install Python 2 and Python 2 library Flask.

——————————————————
2. DATA SOURCE
——————————————————

- We mainly collect the data from 2 websites: UN Data, and World Bank.
- Since we did recognize the correlation between the development of economics and
GDP Incidence, we investigated and got the HIV incidence, total GDP, and total population
data from data.worldbank.org. The detailed link is:
	Males HIV Incidence: http://data.worldbank.org/indicator/SH.HIV.1524.MA.ZS
	Females HIV Incidence: http://data.worldbank.org/indicator/SH.HIV.1524.FE.ZS
	total GDP: http://data.worldbank.org/indicator/NY.GDP.PCAP.CD
	total population: http://data.worldbank.org/indicator/SP.POP.TOTL
- Those data are enough to make correlation, but still not good to make deep analysis. We
then found the data in more details, which is the data about region and income class. These data stipulate which continent, and income class the country in. The link is:
	Income and region: http://data.un.org/Data.aspx?q=HIV&d=UNAIDS&f=inID%3a36
	The data set of above link is HIV, but it also includes the region data. Download the whole set to get region data
- Finally, we find a set of data that contains the population percentage of young males and females (from 15-24) of all countries from 1990 to 2015
	Population Percentage: 

——————————————————
3. DATA PROCESSING
——————————————————

- We first consider how we can pro-process the 5 sets of data to make the main processing stage more flexible and accurate.
	+ We see that in the original data, there were a lot of empty rows and columns.
	Therefore, we copied the data in Google Spreadsheet, delete these empty rows, and columns.
	Finally, we exported these file to csv file again, and downloaded it.
	+ That is the unique method we use to pre-process the data because the data is mainly from same source (except for the region data), and mismatch did not occur
- Next comes to the main data processing stage. We all use Python 2.7 to process the data in this project.
	+ We create a distinct python file called dataProcessing.py to make the project more clear.
	+ Despite that face that, we've already deleted the empty rows and space of the file, we still make the function called cleanData(fileData) to clean some errors
	that we hardly see when manually checking. In this function, we striped all the empty spaces of string, and value of each cells in the data. Subsequently, we
	deleted some countries that did not have any data from 1990 to 2015.
	+ The second function is getData(),  which is also the most important data in this project
		* We import the csv libary if python, to read each csv file by rows, and have the rows data for each csv file
		* The two dictionary data structure will stores and manages all the data in this project. They are yearDict, allCountries. Basically, they stores the same
		data but in reversed order. 
		* In particular, yearDict is a dictionary in which each key is a string ('1990' to '2015') with values being the dictionary. For the dictionary value
		, the key is the name of country, which value is another dictionary which includes 5 distinct keys: malesHIV, femalesHIV, totalGDP, GDPPP(GDP Per Capita)
		, and population. It can be represented as below:
		yearDict: {
			'year': {
				'country': {'malesHIV': value, 'femalesHIV': value,  'totalGDP': value, 'GDPPP': value, 'population': value}
				}
			}
		* Similarly, the allCountries has the same structures as yearDict, but key is country name, and values for year. But in this case, the countries is stoted is
		in dictionary as 'statistics' being key. The countries dictionary also stores the value for income class, sign, and region.
	 	It can be represented as below
		allCountries: {
			'country': {
				'statistics': {
					'year': {'malesHIV': value, 'femalesHIV': value,  'totalGDP': value, 'GDPPP': value, 'population': value}
				},
				'income': value,
				'sign': value,
				'region': value
			}	
	+ After finishing processing data, we passed the data to HTML structure to create the chart, and pivot table by using Flask Framework, or dynamically
	create a JSON file (using AJAX library to get) (Discuss more in part 3)

————————————————————————————
4. STRUCTURE OF WEB PLATFORM
———————————————————————————-

4.1. FRAMEWORK, OUTSOURCED LIBRARY AND API

- We exclusively use flask library in python as framework of the web and to host it in this project
- Besides, we also outsourced some JavaScript Library, and Google API to support some function of the web:
	+ AJAX: We mainly used AJAX to reduce redundant code, and make the function more clear. In particular, we create to fixed template called horizontalMenu.html and footer.html. These two templates exist in almost every page. Therefore, we just use AJAX to get these templates. Besides, we create a distinct js file to process the chart.
Since putting these code in HTML file makes it complicated and difficult to debug and observe, we use GetScript, and GetJSON to make things simple. 
	+ jQuery: This library simplifies some code for actions in this project.
	+ Bootstrap: Split the web page in some parts to strengthen the structure of the web
	+ Google Chart APIs: This is the main tool to make all the charts in the web
	+ Beside, we outsourced some google fonts to make the web more user-friendly (e.g. Roboto, Macondo)
	
4.2. WEB STRUCTURE
- In general, our web contains 5 main pages, each page is represented by one html, and visually supported by at least one css file:
	1. Home (home.html, main CSS: homePage.css) 
		Introduction to the project, problem, features
	2. Pivot Table (pivottable.html, main CSS: pivotTable.css)
		Show the genreal, and detailed pivottable. (Also includes errors handling)
	3. Pivot Table Form (form.html, main CSS: form.css)
		Show the form form which user can choose filter values, row value, column value, and aggregation options
	4. General Chart (generalChart.html, main CSS: generalChart.css)
		Show the two ultimate charts
	5. Observation (observation.html, main CSS: observation.css)
		Show 4 detailed charts and deep analysis
	Besides, all page use general CSS:
		style.css (general style for fonts, padding, margin, and so forth)
		menu.css (css for top menu)
		footer.css (css for footer)

4.3. SUPPORTED FUNCTION (JS & PY FILE)
- Some web page features are supported by at least one js file.
	+ Home page just shows the introduction and features, so it does not have supported js file
	+ Pivot Table page is supported by "pivottableFunction.js", which is passed to html file by AJAX libary
		* In this pivottableFunction.js, there are sort function, draw Bar chart function, switch rows/columns functions and some minor functions
	+ Pivot Table Form page just has 2 minor functions, so we directly includes those function in script tag
	+ General Chart page is supported by "bubblechartProcessing" and "geoChartProcessing.js". The former draw the ultimate bubble chart, and the latter
	draws the ultimate geo chart
	+ Observation page is supported by "drawChartObservation.js". This js file draws 4 different charts for the web. It is important to highlight that
	There are 5 Json file is passed to this web page by GetJSON function (AJAX). These 5 Json file are dynamically processed and created by python file at server side
	and passed to HTML to meet the required form of google chart API. We did not process and create data by JavaScript in this project.
- There are 3 python file that support the main host.py
	+ The first file is "dataProcessing.py" that we've discussed before
	+ The second file is "observationData.py". This file is important since it examine all set of data to get 4 relationship of data. Then it will create the dictionary
	of each obtained set of data to create a JSON file, and then pass to JavaScript to create the chart.
	+ The last file is "pivottableFunction.py" This file manages all the user input in the Pivot Table Form. This file involves some important functions:
		* errorHandlings: This function check all possible errors that users might input, and makes the error description to display in the web page
		* createDescriptions: This functions create the corresponding description for each valid set of inputs entered from the user
		* createDynamicTable: This function is the most important one since it creates the rows and headers for the table from each set of valid inputs
		the user enter. In particular, it filters all the required data, and neflects the others. It then creates a dictionary, in which key is some row labels, and
		values being another dictionary, which includes the values of all filtered values. Then is pass it createHeadersRows functions to create the 
		valid headers and rows for the table (using render_template in Flask)
		* compareData and aggregation are two minor functions that compare data based on the comparision value, aggregated value, and aggregation option


————————————————————————————
5. FOLDER STRUCTURE
———————————————————————————-
In this project, we created total 7 folder, which hold a particular type of filer, but connected tightly to each other.
1. Templates Folder:
	This is the most important folder which involves all the web page templates in this project. It contains two static part of website: horizontal and footer.
2. Css Folder:
	As the name indicates, this folder hold all CSS files which support the design and visualization of the web
3. Data Folder:
	This folder contains all the downloaded data in this project. The host.py will retrieve those data and process them
4. Fonts Folder:
	This folder contains some fonts for the website (including text font and bootstrap fonts)
5. Js Folder:
	This folder contains all the js folder that support some features of the HTML page (Mainly for pivot table and drawing chart)
6. Images Folder:
	This folder contains all the images used in the web
7. Generated Data folder:
	As we said in the previous chapter, the server-side will create the processed Json file to pass to JavaScript to make the pivot chart. The AJAX library is used
	retrieved those data (using get Json)
	
————————————————————————————
6. HOW TO RUN THE WEB
———————————————————————————-
- After going through all the features and the structure of the web, we will show how to host this web. The web is hosted by flask library of Python so that we simply
open the file "host.py" in the folder and run it (using python 2.7). After that, we go to the local domain "http://127.0.0.1:5000/" to start using the website.
- It is worth highlighting that we coded and run this website on the full screen of the computer (>= 1200px). Therefore, to maximize the features and experience of this web, we
suggest you to see the website in full screen (press F11 if you use windows, or click the green expand button on Mac)
- Internet connection is required since the chart (using google API) is created by 
the server on the internet.
——————————————————
7. REFERENCE
——————————————————
- Throughout this project, we have refer to some HTML structure and colors on the internet to create the good-looking and user-friendly webpage:
	+ http://digitalvisitor.com/ : the web that we get some color codes, and refer the menu structure. ( We just observe the structure, and coded by ourselves)
	+ https://color.adobe.com/ : We mainly used this web to adjust the color of our website
	+ https://www.w3schools.com/ : a perfect web to learn from
	+ http://stackoverflow.com/ : a perfect web to get debug hint
	+ https://fonts.google.com/ : all fonts of our website is imported from this website
- The previous student's project:
	+ We slightly refers to the work of last semesters'students on LMS


—————————————————————————————————————————————————————————————————————————————————————————— END ———————————————————————————————————————————————————————————————————————————————





















