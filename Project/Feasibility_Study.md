# Feasibility Study of Group Number 102

**Project Title:** Topics, Cantons and Party Participation in Swiss Parliamentary Business

## 1. Scope and Motivation

This project focuses on parliamentary business in Switzerland. The aim is to analyse which topics are covered in the parliamentary business, how these topics are distributed across the cantons and which political parties participate most often in parliamentary business.

The main purpose of the project is to collect, prepare and analyse real-world data using Python. The data will be collected from the Swiss Parliament through web scraping with Selenium and BeautifulSoup as well as through the Swiss Parliament API. This allows different methods of data collection to be applied and provides practical experience in data cleaning, analysis and visualization with Python.

The topic was selected because the Swiss Parliament provides a large amount of publicly available data. By combining information about parliamentary business with information about council members, the data can be analysed from different perspectives, including topics, cantons and political parties.

## 2. Research Questions

The main research question of the project is: **What patterns can be found in Swiss parliamentary business regarding topics, cantons and political parties?**

To answer this main question, the following three research questions will be examined:

1. Which topics occur most often in completed parliamentary business?
2. How are the topics of completed parliamentary business distributed across the cantons of the involved council members?
3. Which political parties participate most often in parliamentary business?

## 3. Data Source

The project uses one main data source: the official website and data of the Swiss Parliament. Information about parliamentary business is available through Curia Vista (https://www.parlament.ch/de/ratsbetrieb/curia-vista). Relevant information includes the business title, type of business, topic, status, date and the involved person or political actor. The Swiss Parliament also provides information about its council members (https://www.parlament.ch/de/ratsmitglieder?k=*). This includes information such as their name, political party, canton and council. The official Swiss Parliament Open Data Web Services (https://ws-old.parlament.ch/) will also be used to access structured parliamentary data.

## 4. Methodological Approach

The project includes data collection, cleaning, analysis and visualization in Python. Selenium and BeautifulSoup will be used to scrape data from Curia Vista and other subsites of the Swiss Parliament website, including dynamic elements such as filters and search functions. In addition, Python requests will be used to retrieve structured data from the Swiss Parliament API. The API will also be used to compare and validate information collected through web scraping, especially if the scraped data is incomplete.

After the data collection, pandas will be used to check missing values, data types and inconsistent formats. The scraped data and API data will be combined.

Finally, the prepared data will be analysed and visualized in Python. Depending on the results of the analysis, suitable visualizations will be created. Different types of visualizations will be used to present and compare the results of the three research questions.

## 5. Potential Risks and Solutions

During the project, different challenges may occur when collecting, combining and preparing the data. The following risks are considered relevant for the project and possible solutions are described below.

### 5.1 Problems with Web Scraping

The structure of Curia Vista or the Swiss Parliament website could change. Some information may also be loaded dynamically, which could cause problems with the scraper or result in incomplete data.

**Solution:** The scraper will first be tested with a small number of parliamentary businesses. If the structure of the website changes, the Selenium or BeautifulSoup code can be adjusted.

### 5.2 Differences Between Website and API Data

The website and the API provide data from the same source, but the structure and names of the variables may be different. This could make it more difficult to combine the collected information.

**Solution:** The available information from the website and the API will first be compared. Where possible, IDs will be used to connect the data. If needed, columns and values can be renamed or formatted with pandas before combining the data.

### 5.3 Different Political Actors

Not every parliamentary business is submitted by an individual council member. Some businesses may also be submitted by a committee or canton. In these cases, it may not be possible to connect the business to one specific political party or canton.

**Solution:** The type of political actor connected to each business will be checked during the data preparation. For analyses that require information about a canton or political party, only cases with a clear connection will be included. Other cases will be treated separately and mentioned as a limitation of the analysis.

### 5.4 Missing or Incomplete Data

Some information may be missing or incomplete, especially for older parliamentary businesses. It is not yet clear how far back the data can be used with the same level of detail. In addition, information about council members, parties or topics may have changed over time. This could make it difficult to compare older and newer parliamentary business.

**Solution:** The available data will first be checked for different time periods. Based on the completeness of the data, a suitable period for the analysis will be selected. If older data does not contain enough information, the project can focus on more recent years. Missing information will also be checked on both the website and the API.

## 6. Conclusion

The project is considered feasible based on the available data and the planned methods. The next step is to test the data collection through web scraping and the API and to check the quality and completeness of the collected data. Based on these first results, a suitable time period for the analysis can be selected. Overall, the project provides a good opportunity to apply data collection, cleaning, analysis and visualization techniques in Python to real-world parliamentary data.

## 7. Disclaimer: Use of Generative AI

Generative AI may be used during the project to support the programming process, for example to explain error messages or help solve problems in the Python code. It may also provide support when working with web scraping and API requests, as well as for improving the wording of the documentation. The analysis and interpretation of the results and the final conclusions will be carried out by the group members.
